# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_io16_v2.py: IO-16 2.0 plugin

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

from ..tinkerforge.bricklet_io16_v2 import BrickletIO16V2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math
import time
import threading

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde IO-16 Bricklet 2.0 mit Port C
2. Verbinde Testadapter mit IO-16 Bricklet 2.0
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Überprüfe LEDs:
     * Die LEDs blinken gleichzeitig an Port A und B
6. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_state = None
        self.io16 = None
        self.high = True

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_state != None:
            self.cbe_state.set_period(0)

    def get_device_identifier(self):
        return BrickletIO16V2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIO16V2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_state != None:
            self.cbe_state.set_period(0)

        self.io16 = BrickletIO16V2(device_information.uid, self.get_ipcon())
        if self.io16.get_bootloader_mode() != BrickletIO16V2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_state = CallbackEmulator(self.io16.get_value, self.cb_state, ignore_last_data=True)
        self.cbe_state.set_period(1000)

        self.show_device_information(device_information)

    def cb_state(self, _):
        for i in range(16):
            self.io16.set_configuration(i, 'o', self.high)

        self.high = not self.high
