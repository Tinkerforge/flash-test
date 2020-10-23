# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2020 Olaf Lüke <olaf@tinkerforge.com>

bricklet_imu_v3.py: IMU 3.0 plugin

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

from ..tinkerforge.bricklet_imu_v3 import BrickletIMUV3
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Accelerometer Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4  Kalibrieren und Testen im Brick Viewer
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_orientation = None
        self.led_is_on = False

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_orientation != None:
            self.cbe_orientation.set_period(0)

    def get_device_identifier(self):
        return BrickletIMUV3.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIMUV3.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_orientation != None:
            self.cbe_orientation.set_period(0)

        self.imu = BrickletIMUV3(device_information.uid, self.get_ipcon())
        if self.imu.get_bootloader_mode() != BrickletIMUV3.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_orientation = CallbackEmulator(self.imu.get_orientation, self.cb_orientation)
        self.cbe_orientation.set_period(100)

        self.show_device_information(device_information)

    def cb_orientation(self, data):
        self.mw.set_value_normal('Heading: {0}, Roll: {1}, Pitch: {2}'.format(*data))
