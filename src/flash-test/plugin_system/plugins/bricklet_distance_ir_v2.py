# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_distance_ir.py: Distance IR plugin

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

from ..tinkerforge.bricklet_distance_ir_v2 import BrickletDistanceIRV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math
import os

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Wähle korrekten Sensor aus
1. Verbinde Distance IR Bricklet (inklusive Sensor) mit Port C
2. Sensortyp einstellen
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Entfernung wird angezeigt, überprüfe Entfernung
6. Distanz-LED wird heller je näher die Entfernungsmessung
7. Das Bricklet ist fertig, mit Sensor in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_distance = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

        l = self.mw.distance_ir_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)

    def stop(self):
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

        l = self.mw.distance_ir_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

    def get_device_identifier(self):
        return BrickletDistanceIRV2.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletDistanceIRV2.DEVICE_URL_PART))
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)
        
    def new_enum(self, device_information):
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

        self.show_device_information(device_information)
        
        self.distance_ir = BrickletDistanceIRV2(device_information.uid, self.get_ipcon())
        self.distance_ir.set_sensor_type(self.mw.distance_ir_sensor_combo.currentIndex())
        self.cbe_distance = CallbackEmulator(self.distance_ir.get_distance, self.cb_distance)
        self.cbe_distance.set_period(100)
            
    def cb_distance(self, distance):
        self.mw.set_value_normal('Entfernung: ' + str(distance/10) +  'cm')