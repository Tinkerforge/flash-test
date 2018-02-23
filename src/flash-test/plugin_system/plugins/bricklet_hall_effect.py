# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

bricklet_hall_effect.py: Hall Effect plugin

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

from ..tinkerforge.bricklet_hall_effect import BrickletHallEffect
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Hall Effect Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Sensor mit Magnet:
     * Magnet wird erkannt
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    qtcb_state_changed = QtCore.pyqtSignal(int, int, int, int)

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_value = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletHallEffect.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletHallEffect.DEVICE_URL_PART))

    def new_enum(self, device_information):
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.hall_effect = BrickletHallEffect(device_information.uid, self.get_ipcon())
        self.cbe_value = CallbackEmulator(self.hall_effect.get_value, self.cb_value)
        self.cbe_value.set_period(100)

    def cb_value(self, value):
        self.mw.set_value_normal('Magnet ' + ('erkannt' if not value else 'nicht erkannt'))
