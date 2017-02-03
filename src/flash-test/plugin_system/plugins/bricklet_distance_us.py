# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

bricklet_distance_us.py: Distance US plugin

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

from ..tinkerforge.bricklet_distance_us import BrickletDistanceUS
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math
import os

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Distance US Bricklet (inklusive Sensor) mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Entfernungswert wird angezeigt, überprüfe Entfernungswert.
5. Das Bricklet ist fertig, mit Sensor in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_distance_value = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_distance_value != None:
            self.cbe_distance_value.set_period(0)

    def get_device_identifier(self):
        return BrickletDistanceUS.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('distance_us'))
        if self.cbe_distance_value != None:
            self.cbe_distance_value.set_period(0)
        
    def new_enum(self, device_information):
        if self.cbe_distance_value != None:
            self.cbe_distance_value.set_period(0)

        self.show_device_information(device_information)
        
        self.distance_us = BrickletDistanceUS(device_information.uid, self.get_ipcon())
        self.cbe_distance_value = CallbackEmulator(self.distance_us.get_distance_value, self.cb_distance_value)
        self.cbe_distance_value.set_period(100)
            
    def cb_distance_value(self, distance_value):
        self.mw.set_value_normal('Entfernungswert: ' + str(distance_value))
