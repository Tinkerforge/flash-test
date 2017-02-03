# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

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

from PyQt4 import Qt, QtGui, QtCore

from ..tinkerforge.bricklet_industrial_analog_out import BrickletIndustrialAnalogOut
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Analog Out Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert mit Multimeter:
     * Spannung sollte mit angelegter Spannung übereinstimmen
5. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_distance = None
        self.led_is_on = False

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_distance:
            self.cbe_distance.set_period(0)

    def get_device_identifier(self):
        return BrickletIndustrialAnalogOut.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('industrial_analog_out'))

    def new_enum(self, device_information):
        self.industrial_analog_out = BrickletIndustrialAnalogOut(device_information.uid, self.get_ipcon())
        self.industrial_analog_out.set_voltage(10000)
        self.industrial_analog_out.enable()

        self.show_device_information(device_information)
        self.mw.set_value_normal("10V angelegt")
