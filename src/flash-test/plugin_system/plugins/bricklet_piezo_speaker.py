# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Matthias Bolte <matthias@tinkerforge.com>

bricklet_piezo_speaker.py: Piezo Speaker plugin

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

from ..tinkerforge.bricklet_piezo_speaker import BrickletPiezoSpeaker
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

import time
import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Piezo Speaker Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Trenne Master Brick kurz von USB und verbinde Master Brick wieder mit USB
3. Warte bis Master Brick gestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Kalibriere Tonfolge:
   * Es muss ein aufsteigend Tonfolge zu hören sein
6. Das Bricklet ist fertig, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        self.mw.button_calibrate_ps.clicked.connect(self.calibrate_clicked)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        super().stop()
        self.mw.button_calibrate_ps.clicked.disconnect(self.calibrate_clicked)

        l = self.mw.piezo_speaker_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

    def get_device_identifier(self):
        return BrickletPiezoSpeaker.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletPiezoSpeaker.DEVICE_URL_PART))

    def new_enum(self, device_information):
        l = self.mw.piezo_speaker_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)

        self.piezo_speaker = BrickletPiezoSpeaker(device_information.uid, self.get_ipcon())

        self.show_device_information(device_information)

    def calibrate_clicked(self):
        self.piezo_speaker.calibrate()
