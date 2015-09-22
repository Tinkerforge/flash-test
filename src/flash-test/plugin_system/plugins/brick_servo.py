# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

brick_servo.py: Servo plugin

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

from ..tinkerforge.brick_servo import BrickServo
from ..brick_base import BrickBase, get_brick_firmware_filename
from ..callback_emulator import CallbackEmulator

import time

class Plugin(BrickBase):
    TODO_TEXT = u"""\
1. Verbinde Servo Brick mit PC per Mini-USB
2. Falls Brick nicht geflasht wird, drücke "Erase"- und "Reset"-Taster
3. Überprüfe ob Servo sich dreht
3. Gehe zu 1 
"""
    FIRMWARE_FILENAME = get_brick_firmware_filename('servo')

    def start(self, device_information):
        BrickBase.start(self, device_information)

    def get_device_identifier(self):
        return BrickServo.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        self.show_device_information(device_information)
        
        servo = BrickServo(device_information.uid, self.get_ipcon())
        servo.set_velocity(6, 0xFFFF)
        servo.set_position(6, 0)
        servo.enable(6)
        time.sleep(0.5)
        servo.set_position(6, 9000)
        time.sleep(0.5)
        servo.set_position(6, -9000)
