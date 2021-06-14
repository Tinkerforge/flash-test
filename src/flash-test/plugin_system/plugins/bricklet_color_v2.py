# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

bricklet_color_v2.py: Color 2.0 plugin

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

from ..tinkerforge.bricklet_color_v2 import BrickletColorV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Color Bricklet 2.0 mit Port D des Master Bricks 3.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe LED:
     * LED muss leuchten
5. Überprüfe Wert:
     * Wert sollte der Farbe vor dem Sensor entsprechen
6. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_color = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_color != None:
            self.cbe_color.set_period(0)

        l = self.mw.color_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

    def get_device_identifier(self):
        return BrickletColorV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletColorV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_color != None:
            self.cbe_color.set_period(0)

        l = self.mw.color_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)

        self.color = BrickletColorV2(device_information.uid, self.get_ipcon())
        if self.color.get_bootloader_mode() != BrickletColorV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.color.set_light(True)
        self.cbe_color = CallbackEmulator(self.color.get_color, self.cb_color)
        self.cbe_color.set_period(100)

        self.show_device_information(device_information)

    def cb_color(self, color):
        r, g, b, c = color
        normalize = 0xFFFF
        p = self.mw.label_color.palette()
        p.setColor(QtGui.QPalette.Background, QtGui.QColor(r*255.0/normalize, g*255.0/normalize, b*255.0/normalize))
        self.mw.label_color.setPalette(p)

        self.mw.set_value_normal('R: {0}, G: {1}, B: {2}, C: {3}'.format(r, g, b, c))
