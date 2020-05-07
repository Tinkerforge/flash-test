# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2020 Olaf Lüke <olaf@tinkerforge.com>

brick_smartbed.py: Smartbed plugin

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

from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

from ..tinkerforge.ip_connection import base58decode

import os

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Nutze neuen flash adapter!!!
1. Verbinde Smartbed Brick mit flash adapter
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Teste mit Smartbed-Tester
5. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_voltage = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()

    def get_new_uid(self):
        return base58decode('XYZ') # All Smartbed Bricks have UID XYZ

    def get_device_identifier(self):
        return 102

    def flash_clicked(self):
        print("Add correct path to current firmware in:")
        print(os.path.abspath(__file__))
        self.mw.set_value_normal("Add correct path to current firmware in: \n{0}".format(os.path.abspath(__file__)))
#        self.flash_bricklet("/home/olaf/tf/bettzeit/releases/v1_0_2/firmware/mainboard_firmware_v1.0.2.zbin", power_off_duration=0.75)

    def new_enum(self, device_information):
        self.show_device_information(device_information)
        CoMCUBrickletBase.new_enum(self, device_information)
