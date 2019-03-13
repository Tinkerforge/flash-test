# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <matthias@tinkerforge.com>

bricklet_motion_detector_v2.py: Motion Detector plugin

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

from ..tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Motion Detector Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Bewegung sollte nach Aufwärmphase erkannt werden
     * 3 Blaue LEDs sollte müssen im Kreis laufen.
5. Das Bricklet ist fertig, mit schwarzer und weißer Fresnel-Linse in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_motion = None
        self.led = 0

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_motion != None:
            self.cbe_motion.set_period(0)

    def get_device_identifier(self):
        return BrickletMotionDetectorV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletMotionDetectorV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_motion != None:
            self.cbe_motion.set_period(0)

        self.b = BrickletMotionDetectorV2(device_information.uid, self.get_ipcon())
        if self.b.get_bootloader_mode() != BrickletMotionDetectorV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_motion = CallbackEmulator(self.b.get_motion_detected,
                                           self.cb_motion,
                                           ignore_last_data = True)
        self.cbe_motion.set_period(100)

        self.show_device_information(device_information)

    def cb_motion(self, motion):
        if self.led == 0:
            self.led = 1
            self.b.set_indicator(255, 0, 0)
        elif self.led == 1:
            self.led = 2
            self.b.set_indicator(0, 255, 0)
        elif self.led == 2:
            self.led = 0
            self.b.set_indicator(0, 0, 255)

        if motion == 0:
            self.mw.set_value_normal('Keine Bewegung erkannt')
        else:
            self.mw.set_value_okay('Bewegung erkannt!')
