# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

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

from plugin_system.plugin_base import PluginBase

def get_bricklet_firmware_filename(name):
    file_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_directory, '..', '..', '..', 'firmwares', 'bricklets', name, 'bricklet_' + name + '_firmware_latest.bin')

class BrickletBase(PluginBase):    
    def __init__(self, *args):
        PluginBase.__init__(self, *args)

    def start(self, device_information):
        PluginBase.start(self, device_information)

        if device_information != None:
            self.mw.set_tool_status_okay("Plugin gefunden")

            if device_information.uid in ['1', '7xwQ9g']:
                self.mw.set_uid_status_error("Aktuelle UID " + device_information.uid + " ist ungültig")
            else:
                self.mw.set_uid_status_okay("Aktuelle UID lautet " + device_information.uid)

            self.mw.set_flash_status_okay("Aktuelle Firmware Version lautet " + '.'.join([str(fw) for fw in device_information.firmware_version]))
            self.mw.set_value_normal('-')
        else:
            self.mw.set_tool_status_normal("Kein Plugin gefunden")
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')
            self.mw.set_value_normal('-')
