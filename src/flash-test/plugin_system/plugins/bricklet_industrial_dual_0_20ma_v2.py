# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_dual_0_20ma_v2.py: Industrial Dual 0-20mA 2.0

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

from ..tinkerforge.bricklet_industrial_dual_0_20ma_v2 import BrickletIndustrialDual020mAV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Dual 0-20mA Bricklet 2.0 mit Port C
2. Verbinde Strom-Testadapter mit Industrial Dual 0-20mA 2.0 Bricklet
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. 12V am Testadapter einspeisen
5. Überprüfe Ströme:
   * Wert für beide Kanäle sollte ca. 12mA betragen
6. Überprüfe Kanal-LEDs
7. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_current0 = None
        self.cbe_current1 = None
        self.last_current = [0, 0]

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_current0 != None:
            self.cbe_current0.set_period(0)
        if self.cbe_current1 != None:
            self.cbe_current1.set_period(0)

    def get_device_identifier(self):
        return BrickletIndustrialDual020mAV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialDual020mAV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_current0 != None:
            self.cbe_current0.set_period(0)
        if self.cbe_current1 != None:
            self.cbe_current1.set_period(0)

        self.industrial_dual_0_20ma = BrickletIndustrialDual020mAV2(device_information.uid, self.get_ipcon())
        if self.industrial_dual_0_20ma.get_bootloader_mode() != BrickletIndustrialDual020mAV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_current0 = CallbackEmulator(lambda: self.industrial_dual_0_20ma.get_current(0),
                                             lambda c: self.cb_current(0, c))
        self.cbe_current0.set_period(100)

        self.cbe_current1 = CallbackEmulator(lambda: self.industrial_dual_0_20ma.get_current(1),
                                             lambda c: self.cb_current(1, c))
        self.cbe_current1.set_period(100)

        self.show_device_information(device_information)

    def cb_current(self, channel, current):
        self.last_current[channel] = round(current / 1000000.0, 2)
        value = 'Strom Kanal 0: ' + str(self.last_current[0]) + ' mA, Kanal 1: ' + str(self.last_current[1]) + ' mA'

        if self.last_current[0] >= 10 and self.last_current[0] <= 12 and \
           self.last_current[1] >= 10 and self.last_current[1] <= 12:
            self.mw.set_value_okay(value)
        else:
            self.mw.set_value_error(value)
