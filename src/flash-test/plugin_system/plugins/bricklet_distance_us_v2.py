# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

bricklet_distance_us_v2.py: Distance US 2.0 plugin

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

from ..tinkerforge.bricklet_distance_us_v2 import BrickletDistanceUSV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math
import os

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Distance US Bricklet 2.0 mit Flash Adapter XMC
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Entfernung wird angezeigt, überprüfe Entfernung.
5. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_distance = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

    def get_device_identifier(self):
        return BrickletDistanceUSV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletDistanceUSV2.DEVICE_URL_PART))
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

    def new_enum(self, device_information):
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

        self.show_device_information(device_information)

        self.distance_us = BrickletDistanceUSV2(device_information.uid, self.get_ipcon())
        self.cbe_distance = CallbackEmulator(self.distance_us.get_distance, self.cb_distance)
        self.cbe_distance.set_period(100)

    def cb_distance(self, distance):
        self.mw.set_value_normal('Entfernung: {} mm'.format(distance))
