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

from PyQt4 import  QtGui

from plugin_system.plugin_base import PluginBase, base58encode
#from plugin_system.xmc_flash import xmc_flash
from plugin_system.xmc_flash_by_master import xmc_flash, xmc_write_firmwares_to_ram
from .tinkerforge.brick_master import BrickMaster
from .tinkerforge.brick_master_flash_adapter_xmc import BrickMasterFlashAdapterXMC
from .tinkerforge.bricklet_industrial_quad_relay import BrickletIndustrialQuadRelay
from .tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from .tinkerforge.ip_connection import IPConnection

from zipfile import ZipFile
import traceback
import time
import os
import sys
from subprocess import Popen, PIPE
import fcntl

MASK_NONE  = 0b0000
MASK_POWER = 0b0010
MASK_DATA  = 0b0001

CONFIG_BAUDRATE   = 115200
CONFIG_TTY        = '/dev/ttyUSB0'
CONFIG_UID_IQR    = '555'

def get_bricklet_firmware_filename(name):
    file_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_directory, '..', '..', '..', 'firmwares', 'bricklets', name, 'bricklet_' + name + '_firmware_latest.zbin')

class CoMCUBrickletBase(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, *args)
        
        self.comcu_uid_to_flash = None

    def start(self, device_information):
        self.mw.button_continue.hide()
        PluginBase.start(self, device_information)
        self.show_device_information(device_information, clear_value=True)

    def show_device_information(self, device_information, clear_value=False):
        if device_information != None:
            self.mw.set_tool_status_okay("Plugin gefunden")

            if device_information.uid in ['1', '7xwQ9g']:
                self.mw.set_uid_status_error("Aktuelle UID " + device_information.uid + " ist ungültig")
            else:
                self.mw.set_uid_status_okay("Aktuelle UID lautet " + device_information.uid)

            self.mw.set_flash_status_okay("Aktuelle Firmware Version lautet " + '.'.join([str(fw) for fw in device_information.firmware_version]))
        else:
            self.mw.set_tool_status_normal("Kein Plugin gefunden")
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')

        if clear_value:
            self.mw.set_value_normal('-')
            
    def new_enum(self, device_information):
        self.comcu_uid_to_flash = device_information.uid
            
    def flash_bricklet(self, plugin_filename):
        self.comcu_uid_to_flash = None
        bootloader_success = self.write_bootloader_to_bricklet(plugin_filename)
        firmware_success = self.write_firmware_and_uid_to_bricklet(plugin_filename)

        if bootloader_success and firmware_success:
            pass
            
    def write_firmware_and_uid_to_bricklet(self, plugin_filename):
        start = time.time()
        while self.comcu_uid_to_flash == None:
            if time.time() - start > 3:
                self.mw.set_flash_status_error('Timeout beim Firmware schreiben')
                return False
            QtGui.QApplication.processEvents()
            
        try:
            self.mw.set_flash_status_action('Starting bootloader mode')

            try:
                zf = ZipFile(plugin_filename, 'r')
            except:
                self.mw.set_flash_status_error('Could not open Bricklet plugin:\n\n' + traceback.format_exc())
                return False

            plugin_data = None
            for name in zf.namelist():
                if name.endswith('firmware.bin'):
                    plugin_data = zf.read(name)
                    break

            if plugin_data == None:
                self.mw.set_flash_status_error('Could not find firmware in zbin')
                return False

            # Now convert plugin to list of bytes
            plugin = plugin_data
            regular_plugin_upto = -1
            for i in reversed(range(4, len(plugin)-12)):
                if plugin[i] == 0x12 and plugin[i-1] == 0x34 and plugin[i-2] == 0x56 and plugin[i-3] == 0x78:
                    regular_plugin_upto = i
                    break

            if regular_plugin_upto == -1:
                self.mw.set_flash_status_error('Could not find magic number in firmware')

            ipcon = IPConnection()
            device = BrickletGPSV2(self.comcu_uid_to_flash, ipcon)
            ipcon.connect('localhost', 4223)

            device.set_bootloader_mode(device.BOOTLOADER_MODE_BOOTLOADER)
            counter = 0
            while True:
                try:
                    if device.get_bootloader_mode() == device.BOOTLOADER_MODE_BOOTLOADER:
                        break
                except:
                    pass

                if counter == 10:
                    self.mw.set_flash_status_error('Device did not enter bootloader mode in 2.5s')
                    return False

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

            self.mw.set_flash_status_action('Schreibe Firmware: ' + name)
            for position in index_list:
                start = position*64
                end   = (position+1)*64
                self.mw.set_flash_status_action('Schreibe Firmware: ' + str(position) + '/' + str(num_packets-1))
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
                
                self.mw.set_flash_status_error('Coud not change from bootloader mode to firmware mode: ' + error_str)
                return False
                
            counter = 0
            while True:
                try:
                    bootloader_mode = device.get_bootloader_mode()
                    if bootloader_mode == device.BOOTLOADER_MODE_FIRMWARE:
                        break
                except:
                    import traceback
                    traceback.print_exc()
                    pass

                if counter == 10:
                    self.mw.set_flash_status_error('Device did not enter firmware mode in 2.5s')
                    return False

                time.sleep(0.25)
                counter += 1

            self.mw.set_flash_status_okay('Firmware geschrieben und gestartet')
            
            try:
                uid = int(self.get_new_uid())
            except:
                traceback.print_exc()
                self.mw.set_uid_status_error('Konnte keine neue UID von tinkerforge.com abfragen')
                return False
            
            try:
                device.write_uid(uid)
                uid_read = device.read_uid()
                if uid != uid_read:
                    self.mw.set_uid_status_error("Konnte UID nicht verifizieren")
                    return False
            except:
                traceback.print_exc()
                self.mw.set_uid_status_error('Konnte UID nicht setzen')
                return False

            self.mw.set_uid_status_okay('Neue UID "' + base58encode(uid) + '" gesetzt')
            
            self.comcu_uid_to_flash = None
            
            BrickMasterFlashAdapterXMC(self.mw.device_manager.flash_adapter_xmc_uid, ipcon).reset()
            return True
            
        except:
            self.mw.set_flash_status_error('Unexpected error:\n\n' + traceback.format_exc())
            return False
            
    def write_bootloader_to_bricklet(self, plugin_filename):
        uid_master = self.mw.device_manager.flash_adapter_xmc_uid
        if uid_master == None:
            self.mw.set_flash_status_error('Flash Adapter XMC nicht angeschlossen')
            return False

        ipcon = IPConnection()
        iqr = BrickletIndustrialQuadRelay(CONFIG_UID_IQR, ipcon)
        master = BrickMasterFlashAdapterXMC(uid_master, ipcon)

        ipcon.connect('localhost', 4223)

        self.mw.set_flash_status_action("Schreibe Bootstrapper und -loader")
        i = 2
        
        try:
            xmc_write_firmwares_to_ram(plugin_filename, master, non_standard_print=self.mw.set_flash_status_action)
        except Exception as e:
            self.mw.set_flash_status_error(str(e))
            ipcon.disconnect()
            return False

        start = time.time()
        ret = True
        while True:
            if time.time() - start > 3:
                self.mw.set_flash_status_error('Timeout beim Bootloader schreiben')
                ret = False
                break
            
            if i == 2:
                iqr.set_value(MASK_NONE | MASK_DATA)
                time.sleep(0.1)
                iqr.set_value(MASK_POWER)
                i = 0

            i += 1
            try:
                time.sleep(0.01)
                xmc_flash(master)
                break
            except Exception as e:
                self.mw.set_flash_status_error(str(e))
            
        iqr.set_value(MASK_POWER)
        master.reset()
        ipcon.disconnect()
        
        return ret

    def write_new_uid_to_bricklet(self):
        try:
            uid = base58encode(int(self.get_new_uid()))
        except:
            traceback.print_exc()
            self.mw.set_uid_status_error('Konnte keine neue UID von tinkerforge.com abfragen')
            return False
        
        return True