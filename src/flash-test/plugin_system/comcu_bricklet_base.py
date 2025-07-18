# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_base.py: Base for Bricklets

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from plugin_system.plugin_base import PluginBase, base58encode
from plugin_system.xmc_flash_bootloader import xmc_flash_bootloader
from plugin_system.util import LabelInfo
from .tinkerforge.brick_master import BrickMaster
from .tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from .tinkerforge.bricklet_unknown import BrickletUnknown
from .tinkerforge.ip_connection import IPConnection

from zipfile import ZipFile
import traceback
import time
import os
import sys
from subprocess import Popen, PIPE
import fcntl

def get_bricklet_firmware_filename(name):
    file_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_directory, '..', '..', '..', 'firmwares', 'bricklets', name, 'bricklet_' + name + '_firmware_latest.zbin')

class CoMCUBrickletBase(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, *args)

        self.comcu_uid_to_flash = None

    def start(self):
        self.mw.check_print_label.show()
        self.mw.button_continue.hide()
        PluginBase.start(self)
        self.show_device_information(None, clear_value=True)

    def show_device_information(self, device_information, clear_value=False):
        if device_information != None:
            self.mw.set_tool_status_okay("Plugin found")

            if device_information.uid in ['1', '7xwQ9g']:
                self.mw.set_uid_status_error("Current UID " + device_information.uid + " is invalid")
            else:
                self.mw.set_uid_status_okay("Current UID is " + device_information.uid)

            self.mw.set_flash_status_okay("Installed firmware version is " + '.'.join([str(fw) for fw in device_information.firmware_version]))
        else:
            self.mw.set_tool_status_normal("No plugin found")
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')

        if clear_value:
            self.mw.set_value_normal('-')

    def new_enum(self, device_information):
        self.comcu_uid_to_flash = device_information.uid

    def is_comcu(self):
        return True

    def flash_bricklet(self, plugin_filename, power_off_duration=None, sku_override=None, try_count=None):
        self.comcu_uid_to_flash = None
        bootloader_success = self.write_bootloader_to_bricklet(plugin_filename, power_off_duration=power_off_duration, try_count=try_count)
        firmware_success, label_info = self.write_firmware_and_uid_to_bricklet(plugin_filename, sku_override=sku_override)

        if bootloader_success and firmware_success:
            if self.mw.check_print_label.isChecked():
                self.mw.print_label(label_info)

        return bootloader_success and firmware_success

    def write_firmware_and_uid_to_bricklet(self, plugin_filename, sku_override=None):
        start = time.time()
        while self.comcu_uid_to_flash == None:
            if time.time() - start > 10:
                self.mw.set_flash_status_error('Writing firmware timed out')
                return False, None
            QtWidgets.QApplication.processEvents()

        try:
            self.mw.set_flash_status_action('Starting bootloader mode')

            try:
                zf = ZipFile(plugin_filename, 'r')
            except:
                self.mw.set_flash_status_error('Failed to open Bricklet plugin:\n\n' + traceback.format_exc())
                return False, None

            plugin_data = None
            for name in zf.namelist():
                if name.endswith('firmware.bin'):
                    plugin_data = zf.read(name)
                    break

            if plugin_data == None:
                self.mw.set_flash_status_error('Failed to find firmware in zbin')
                return False, None

            # Now convert plugin to list of bytes
            plugin = plugin_data
            regular_plugin_upto = -1
            for i in reversed(range(4, len(plugin)-12)):
                if plugin[i] == 0x12 and plugin[i-1] == 0x34 and plugin[i-2] == 0x56 and plugin[i-3] == 0x78:
                    regular_plugin_upto = i
                    break

            if regular_plugin_upto == -1:
                self.mw.set_flash_status_error('Failed to find "magic number" in firmware')

            ipcon = IPConnection()
            device = BrickletUnknown(self.comcu_uid_to_flash, ipcon)
            device.set_response_expected_all(True)
            ipcon.connect('localhost', 4223)

            device.set_bootloader_mode(device.BOOTLOADER_MODE_BOOTLOADER)
            counter = 0
            last_exc_tup = None
            while True:
                try:
                    if device.get_bootloader_mode() == device.BOOTLOADER_MODE_BOOTLOADER:
                        break
                except:
                    last_exc_tup = sys.exc_info()

                if counter == 10:
                    self.mw.set_flash_status_error('Device not in bootloader mode after 2,5 s.')
                    traceback.print_exception(*last_exc_tup)
                    QMessageBox.critical(self.mw, 'Device not in bootloader mode after 2,5 s.', 'Device not in bootloader mode after 2,5 s\nSee traceback in terminal.')
                    ipcon.disconnect()
                    return False, None

                time.sleep(0.25)
                counter += 1

            num_packets = len(plugin)//64
            # If the magic number is in in the last page of the
            # flash, we write the whole thing
            if regular_plugin_upto >= (len(plugin) - 64*4):
                index_list = list(range(num_packets))
            else:
                # We write the 64 byte packets up to the end of the last page that has meaningful data
                packet_up_to = ((regular_plugin_upto // 256)+1)*4
                index_list = list(range(0, packet_up_to)) + [num_packets-4, num_packets-3, num_packets-2, num_packets-1]

            # The expected pattern is not pre-written in the xmc 1400,
            # so we need to rewrite the complete flash
            xmc_1400_bricklets = [
                'bricklet_air_quality',
                'bricklet_can_v2',
                'bricklet_dmx',
                'bricklet_e_paper_296x128',
                'bricklet_industrial_counter',
                'bricklet_particulate_matter',
                'bricklet_rs485',
                'bricklet_rs232_v2',
                'bricklet_sound_pressure_level'
            ]
            if any(xmc_1400_bricklet in plugin_filename for xmc_1400_bricklet in xmc_1400_bricklets):
                index_list = range(num_packets)

            for _ in range(2):
                if _ == 1:
                    index_list = range(num_packets)

                self.mw.set_flash_status_action('Writing firmware: ' + name)
                to_write = str(len(index_list) - 1)
                for position in index_list:
                    start = position*64
                    end   = (position+1)*64
                    self.mw.set_flash_status_action('Writing firmware: ' + str(position) + '/' + to_write)
                    device.set_write_firmware_pointer(start)
                    device.write_firmware(plugin[start:end])

                self.mw.set_flash_status_action('Changing from bootloader mode to firmware mode')

                mode_ret = device.set_bootloader_mode(device.BOOTLOADER_MODE_FIRMWARE)
                if mode_ret != 0 and mode_ret != 2: # 0 = ok, 2 = no change
                    error_str = ''
                    if mode_ret == 1:
                        error_str = 'Invalid mode (Error 1)'
                    elif mode_ret == 3:
                        error_str = 'Entry function not present (Error 3)'
                    elif mode_ret == 4:
                        error_str = 'Device identifier incorrect (Error 4)'
                    elif mode_ret == 5:
                        error_str = 'CRC Mismatch (Error 5)'
                    else: # unkown error case
                        error_str = 'Error ' + str(mode_ret)

                    # In case of CRC Mismatch we try a second time
                    if mode_ret == 5:
                        continue

                    self.mw.set_flash_status_error('Failed to change from bootloader mode to firmware mode: ' + error_str)
                    ipcon.disconnect()
                    return False, None

                # Everything OK, we dont have to try a second time
                break

            counter = 0
            last_exc_tup = None
            while True:
                try:
                    bootloader_mode = device.get_bootloader_mode()
                    if bootloader_mode == device.BOOTLOADER_MODE_FIRMWARE:
                        break
                except:
                    last_exc_tup = sys.exc_info()

                if counter == 10:
                    self.mw.set_flash_status_error('Device not in firmware mode after 2,5 s.')
                    traceback.print_exception(*last_exc_tup)
                    QMessageBox.critical(self.mw, 'Device not in firmware mode after 2,5 s.', 'Device not in firmware mode after 2,5 s\nSee traceback in terminal.')
                    ipcon.disconnect()
                    return False, None

                time.sleep(0.25)
                counter += 1

            self.mw.set_flash_status_okay('Firmware written and booted')

            try:
                uid = int(self.get_new_uid())
            except:
                traceback.print_exc()
                self.mw.set_uid_status_error('Konnte keine neue UID von tinkerforge.com abfragen')
                QMessageBox.critical(self.mw, "Konnte keine neue UID von tinkerforge.com abfragen.", "Konnte keine neue UID von tinkerforge.com abfragen:\nSee traceback in terminal.")
                ipcon.disconnect()
                return False, None

            try:
                identity = device.get_identity()
            except:
                traceback.print_exc()
                self.mw.set_uid_status_error('Failed to query device identity')
                QMessageBox.critical(self.mw, "Failed to query device identity.", "Failed to query device identity:\nSee traceback in terminal.")
                ipcon.disconnect()
                return False, None

            try:
                device.write_uid(uid)
                if not 'bricklet_isolator_firmware' in plugin_filename:
                    uid_read = device.read_uid()
                    if uid != uid_read:
                        self.mw.set_uid_status_error("Failed to verify UID")
                        ipcon.disconnect()
                        return False, None
            except:
                traceback.print_exc()
                self.mw.set_uid_status_error('Failed to set UID')
                QMessageBox.critical(self.mw, "Failed to set UID.", "Failed to set UID:\nSee traceback in terminal.")
                ipcon.disconnect()
                return False, None

            self.mw.set_uid_status_okay('Set new UID ' + base58encode(uid))

            self.comcu_uid_to_flash = None

            BrickMaster(self.mw.device_manager.flash_master_brick_v3_uid, ipcon).reset()

            self.mw.increase_flashed_count()

            if sku_override != None:
                sku = sku_override
            else:
                sku = identity.device_identifier

            ipcon.disconnect()
            return True, LabelInfo(sku, base58encode(uid), identity.firmware_version, None)
        except:
            traceback.print_exc()
            self.mw.set_flash_status_error('Unexpected error:\n\n' + traceback.format_exc())
            return False, None

    def write_bootloader_to_bricklet(self, plugin_filename, power_off_duration=None, try_count=None):
        uid_master = self.mw.device_manager.flash_master_brick_v3_uid
        if uid_master == None:
            self.mw.set_flash_status_error('No Master Brick >= 3.0 connected')
            return False

        try:
            return xmc_flash_bootloader(plugin_filename, uid_master=uid_master,
                                        non_standard_print=self.mw.set_flash_status_action,
                                        power_off_duration=power_off_duration, try_count=try_count)
        except Exception as e:
            self.mw.set_flash_status_error(str(e))
            return False
