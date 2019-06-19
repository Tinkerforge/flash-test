# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_io4_v2.py: IO-4 2.0 plugin

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

from ..tinkerforge.bricklet_io4_v2 import BrickletIO4V2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math
import time

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde IO-4 Bricklet 2.0 mit Port C
2. Verbinde Testadapter mit IO-4 Bricklet 2.0
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Überprüfe LEDs:
     * Die LEDs leuchten der Reihe nach auf
6. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_value = None
        self.state = 0

    def start(self):
        CoMCUBrickletBase.start(self)

    def get_device_identifier(self):
        return BrickletIO4V2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIO4V2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        self.show_device_information(device_information)

        self.io4_v2 = BrickletIO4V2(device_information.uid, self.get_ipcon())
        if self.io4_v2.get_bootloader_mode() != BrickletIO4V2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_value = CallbackEmulator(self.io4_v2.get_value, self.cb_value, ignore_last_data=True)
        self.cbe_value.set_period(200)

    def cb_value(self, value):
        if self.state == 0:
            self.io4_v2.set_configuration(0, 'o', True)
            self.io4_v2.set_configuration(1, 'o', False)
            self.io4_v2.set_configuration(2, 'o', False)
            self.io4_v2.set_configuration(3, 'o', False)
        elif self.state == 1:
            self.io4_v2.set_configuration(0, 'o', False)
            self.io4_v2.set_configuration(1, 'o', True)
            self.io4_v2.set_configuration(2, 'o', False)
            self.io4_v2.set_configuration(3, 'o', False)
        elif self.state == 2:
            self.io4_v2.set_configuration(0, 'o', False)
            self.io4_v2.set_configuration(1, 'o', False)
            self.io4_v2.set_configuration(2, 'o', True)
            self.io4_v2.set_configuration(3, 'o', False)
        elif self.state == 3:
            self.io4_v2.set_configuration(0, 'o', False)
            self.io4_v2.set_configuration(1, 'o', False)
            self.io4_v2.set_configuration(2, 'o', False)
            self.io4_v2.set_configuration(3, 'o', True)

        self.state = (self.state + 1) % 4
