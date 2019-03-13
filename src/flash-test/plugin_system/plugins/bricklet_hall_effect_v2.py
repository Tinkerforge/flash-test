# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_hall_effect_v2.py: Hall Effect 2.0 plugin

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

from ..tinkerforge.bricklet_hall_effect_v2 import BrickletHallEffectV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Hall Effect Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Sensor mit Magnet:
     * Magnet von unten sollte Wert < -7000 liefern
     * Magnet von oben sollte Wert > 7000 liefern
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_value = None
        self.reached_negative = False
        self.reached_positive = False

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletHallEffectV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletHallEffectV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_value != None:
            self.cbe_value.set_period(0)
        self.reached_negative = False
        self.reached_positive = False

        self.hall_effect = BrickletHallEffectV2(device_information.uid, self.get_ipcon())
        if self.hall_effect.get_bootloader_mode() != BrickletHallEffectV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_value = CallbackEmulator(self.hall_effect.get_magnetic_flux_density, self.cb_value)
        self.cbe_value.set_period(100)

    def cb_value(self, value):
        if value <= -7000:
            self.reached_negative = True
        if value >= 7000:
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

        call('Wert: ' + str(value) + 'uT | neg: ' + neg + ' | pos: ' + pos)
