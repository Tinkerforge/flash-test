# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

bricklet_rotary_poti.py: Rotary Poti plugin

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

from ..tinkerforge.bricklet_rotary_poti import BrickletRotaryPoti
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Rotary Poti Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Poti:
     * Drehe bis -150
     * Drehe bis +150
5. Das Bricklet ist fertig, zusammen mit Knopf in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_position = None
        self.reached_negative = False
        self.reached_positive = False

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        super().stop()
        if self.cbe_position != None:
            self.cbe_position.set_period(0)

    def get_device_identifier(self):
        return BrickletRotaryPoti.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletRotaryPoti.DEVICE_URL_PART))

    def new_enum(self, device_information):
        if self.cbe_position != None:
            self.cbe_position.set_period(0)

        self.reached_negative = False
        self.reached_positive = False

        self.rotary_poti = BrickletRotaryPoti(device_information.uid, self.get_ipcon())
        self.cbe_position = CallbackEmulator(self.rotary_poti.get_position,
                                             self.cb_position,
                                             ignore_last_data=True)
        self.cbe_position.set_period(25)

        self.show_device_information(device_information)

    def cb_position(self, position):
        if position <= -150:
            self.reached_negative = True
        if position >= 150:
            self.reached_positive = True

        neg = '\u25C7'
        pos = '\u25C7'
        if self.reached_negative:
            neg = '\u25C6'
        if self.reached_positive:
            pos = '\u25C6'

        if self.reached_negative and self.reached_positive:
            call = self.mw.set_value_okay
        else:
            call = self.mw.set_value_action

        call('Wert: ' + str(position) + ' | -150: ' + neg + ' | +150: ' + pos)
