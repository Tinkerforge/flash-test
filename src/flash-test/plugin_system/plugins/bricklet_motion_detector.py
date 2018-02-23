# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <matthias@tinkerforge.com>

bricklet_motion_detector.py: MotionDetector plugin

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

from ..tinkerforge.bricklet_motion_detector import BrickletMotionDetector
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
0. Stecke Bewegungsmelder auf Motion Detector Bricklet
1. Verbinde Motion Detector Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Bewegung sollte nach Aufwärmphase erkannt werden
     * Blaue LED sollte aktiviert werden wenn Bewegung erkannt wird
5. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_motion = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_motion != None:
            self.cbe_motion.set_period(0)

    def get_device_identifier(self):
        return BrickletMotionDetector.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletMotionDetector.DEVICE_URL_PART))

    def new_enum(self, device_information):
        if self.cbe_motion != None:
            self.cbe_motion.set_period(0)

        self.b = BrickletMotionDetector(device_information.uid, self.get_ipcon())
        self.cbe_motion = CallbackEmulator(self.b.get_motion_detected,
                                           self.cb_motion)
        self.cbe_motion.set_period(100)

        self.show_device_information(device_information)

    def cb_motion(self, motion):
        if motion == 0:
            self.mw.set_value_normal('Keine Bewegung erkannt')
        else:
            self.mw.set_value_okay('Bewegung erkannt!')
