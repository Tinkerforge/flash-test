# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

extension_base.py: Base for Extensions

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

from plugin_system.plugin_base import PluginBase

from PyQt4 import QtCore

import os
import time
import threading

def get_extension_firmware_filename(name, extension='bin'):
    file_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_directory, '..', '..', '..', 'firmwares', 'extensions', name, 'extension_' + name + '_firmware_latest.' + extension)

class ExtensionBase(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, *args)

    def start(self, device_information):
        self.mw.button_flash.setEnabled(False)
        PluginBase.start(self, device_information)
        self.mw.set_tool_status_okay("-")
        self.mw.set_uid_status_okay("-")
        self.mw.set_flash_status_okay("-")
        self.mw.set_value_normal('-')
        self.mw.button_continue.hide()

    def stop(self):
        self.mw.button_flash.setEnabled(True)
        PluginBase.stop(self)
