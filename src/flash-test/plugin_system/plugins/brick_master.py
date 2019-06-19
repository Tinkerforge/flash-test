# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

brick_master.py: Master plugin

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

from ..tinkerforge.brick_master import BrickMaster
from ..brick_base import BrickBase, get_brick_firmware_filename

class Plugin(BrickBase):
    TODO_TEXT = u"""
1. Verbinde Master Brick mit PC per Mini-USB
2. Falls Brick nicht automatisch geflasht wird, drücke "Erase"- und "Reset"-Taster
3. Blaue LED neben Mini-USB buchse muss leuchten, 4 blaue LEDs an der Seite
   müssen einmal Lauflicht anzeigen
4. Gehe zu 1

* Weitere Tests (Stapel und Extension) findet im Brick Viewer statt
"""
    FIRMWARE_FILENAME = get_brick_firmware_filename(BrickMaster.DEVICE_URL_PART)

    def start(self):
        BrickBase.start(self)

    def get_device_identifier(self):
        return BrickMaster.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        self.show_device_information(device_information)
