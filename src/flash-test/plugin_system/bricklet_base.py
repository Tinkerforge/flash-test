# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015-2017 Olaf Lüke <olaf@tinkerforge.com>

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

import os
import traceback

from PyQt5.QtWidgets import QMessageBox

from plugin_system.plugin_base import PluginBase, base58encode
from .tinkerforge.brick_master import BrickMaster
from .tinkerforge.ip_connection import IPConnection

def get_bricklet_firmware_filename(name):
    file_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_directory, '..', '..', '..', 'firmwares', 'bricklets', name, 'bricklet_' + name + '_firmware_latest.bin')

class BrickletBase(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, *args)

    def start(self):
        self.mw.check_print_label.hide()
        self.mw.button_continue.hide()
        PluginBase.start(self)
        self.show_device_information(None, clear_value=True)

    def show_device_information(self, device_information, clear_value=False):
        if device_information != None:
            self.mw.set_tool_status_okay("Plugin foubd")

            if device_information.uid in ['1', '7xwQ9g']:
                self.mw.set_uid_status_error("Current UID " + device_information.uid + " is invalid")
            else:
                self.mw.set_uid_status_okay("Current UID lautet " + device_information.uid)

            self.mw.set_flash_status_okay("Current firmware version is " + '.'.join([str(fw) for fw in device_information.firmware_version]))
        else:
            self.mw.set_tool_status_normal("No plugin found")
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')

        if clear_value:
            self.mw.set_value_normal('-')

    def write_plugin_to_bricklet(self, plugin_filename):
        try:
            port = 'c'
            plugin = open(plugin_filename, mode='rb').read()
            plugin_chunk_size = 32
            plugin_chunks = []
            offset = 0
            ipcon = self.get_ipcon()
            master = self.get_current_master()

            while offset < len(plugin):
                chunk = plugin[offset:offset + plugin_chunk_size]

                if len(chunk) < plugin_chunk_size:
                    chunk += b'\0' * (plugin_chunk_size - len(chunk))

                chunk = list(chunk)

                plugin_chunks.append(chunk)
                offset += plugin_chunk_size

            position = 0
            for chunk in plugin_chunks:
                master.write_bricklet_plugin(port, position, chunk)

                position += 1

                self.mw.set_flash_status_action("Writing port " + port.upper() +  ": " + str(position) + '/' + str(len(plugin_chunks)))

            position = 0
            for chunk in plugin_chunks:
                self.mw.set_flash_status_action("Verifying port " + port.upper() + ": " + str(position) + '/' + str(len(plugin_chunks)))
                read_chunk = list(master.read_bricklet_plugin(port, position))

                if read_chunk != chunk:
                    self.mw.set_flash_status_error("Failed to verify plugin at port " + port.upper())
                    return False
                position += 1
        except:
            traceback.print_exc()
            QMessageBox.critical(self.mw, "Failed to write plugin.", "Failed to write plugin: \n{}\nSee traceback in terminal.".format(self.mw.label_flash_status.text()))
            return False

        self.mw.set_flash_status_okay("Plugin at port " + port.upper() + ' written and verified')
        self.mw.increase_flashed_count()
        return True

    def write_new_uid_to_bricklet(self):
        try:
            uid = base58encode(int(self.get_new_uid()))
        except:
            traceback.print_exc()
            self.mw.set_uid_status_error('Failed to get new UID')
            QMessageBox.critical(self.mw, "Failed to get new UID.", "Failed to get new UID: \nSee traceback in terminal.")
            return False

        try:
            port = 'c'
            self.get_ipcon().write_bricklet_uid(self.get_current_master(), port, uid)
            uid_read = self.get_ipcon().read_bricklet_uid(self.get_current_master(), port)
            if uid != uid_read:
                self.mw.set_uid_status_error("Failed to verify UID at port " + port.upper())
                return False
        except:
            traceback.print_exc()
            self.mw.set_uid_status_error('Failed to set UID for port ' + port.upper())
            QMessageBox.critical(self.mw, 'Failed to set UID for port ' + port.upper(), 'Failed to set UID for port ' + port.upper()": \nSee traceback in terminal.")
            return False

        self.mw.set_uid_status_okay('New UID "' + uid + '" for port ' + port.upper() + ' set')
        return True
