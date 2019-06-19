# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

brick_dc.py: DC plugin

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

from ..tinkerforge.brick_dc import BrickDC
from ..brick_base import BrickBase, get_brick_firmware_filename

import time

class Plugin(BrickBase):
    TODO_TEXT = u"""\
0. Baue Netzteil auf, verbinde Motor mit Netzteil und stelle Spannung auf 10V.
1. Stecke Motor (mit grünem und schwarzem Stecker) in DC Brick
2. Verbinde DC Brick mit PC per Mini-USB
3. Falls Brick nicht geflasht wird, drücke "Erase"- und "Reset"-Taster
4. Überprüfe ob Motor sich dreht (3 Sekunden Beschleunigung mit anschließender Debeschleunigung)
5. Das Brick ist fertig, mit schwarzem und grünen 2-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben*
6. Gehe zu 1

Zusätzlich:
 * 1. Stapeltest mit 1x Master Brick, 8x DC Brick und 2x Extension.
 * 2. Kühlkörper aufkleben
"""
    FIRMWARE_FILENAME = get_brick_firmware_filename(BrickDC.DEVICE_URL_PART)

    def start(self):
        BrickBase.start(self)

    def get_device_identifier(self):
        return BrickDC.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        self.show_device_information(device_information)

        dc = BrickDC(device_information.uid, self.get_ipcon())
        dc.set_pwm_frequency(10000)
        dc.set_drive_mode(0)
        dc.enable()
        dc.set_acceleration(10000)
        dc.set_velocity(32767)
        time.sleep(3)
        dc.set_velocity(0)
        dc.disable()
