# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2022 Matthias Bolte <matthias@tinkerforge.com>

label_brick_wo_master.py: Brick w/o Master Brick label print plugin

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

from PyQt5 import Qt, QtGui, QtCore

from ..util import LabelInfo
from ..tinkerforge.brick_master import BrickMaster
from ..plugin_base import PluginBase

import traceback

class Plugin(PluginBase):
    TODO_TEXT = u"""\
1. Verbinde fertigen Brick mit PC per USB
2. Etikett wird automatisch gedruckt (Master Bricks werden ignoriert)
"""

    def start(self):
        self.mw.button_flash.setEnabled(False)
        self.mw.check_print_label.show()
        self.mw.button_continue.hide()
        PluginBase.start(self)
        self.show_device_information(None, clear_value=True)

    def show_device_information(self, device_information, clear_value=False):
        if device_information != None:
            self.mw.set_tool_status_okay("Firmware found")
            self.mw.set_uid_status_okay("Current UID is " + device_information.uid)
            self.mw.set_flash_status_okay("Installed firmware version is " + '.'.join([str(fw) for fw in device_information.firmware_version]))
        else:
            self.mw.set_tool_status_normal("No firmware found")
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')

        self.mw.button_continue.hide()

        if clear_value:
            self.mw.set_value_normal('-')

    def handles_device_identifier(self, device_identifier):
        return str(device_identifier).startswith('1') and device_identifier != BrickMaster.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        self.show_device_information(device_information)

        if self.mw.check_print_label.isChecked():
            self.mw.print_label(LabelInfo(device_information.device_identifier, device_information.uid, device_information.firmware_version, device_information.hardware_version))
