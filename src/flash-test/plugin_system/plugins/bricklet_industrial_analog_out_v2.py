# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_analog_out.py: Industrial Analog Out plugin

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

from ..tinkerforge.bricklet_industrial_analog_out_v2 import BrickletIndustrialAnalogOutV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Analog Out Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert mit zwei Multimeter:
     * Spannung sollte 10V sein
     * Strom sollte 20mA sein
5. Überprüfe Kanal-LEDs
6. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.led_is_on = False

    def start(self):
        CoMCUBrickletBase.start(self)

    def get_device_identifier(self):
        return BrickletIndustrialAnalogOutV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialAnalogOutV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.industrial_analog_out = BrickletIndustrialAnalogOutV2(device_information.uid, self.get_ipcon())
        if self.industrial_analog_out.get_bootloader_mode() != BrickletIndustrialAnalogOutV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.industrial_analog_out.set_voltage(10000)
        self.industrial_analog_out.set_enabled(True)

        self.show_device_information(device_information)
        self.mw.set_value_normal("10V/20mA angelegt")
