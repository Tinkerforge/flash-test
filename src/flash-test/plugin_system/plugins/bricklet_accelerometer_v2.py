# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_accelerometer_v2.py: Accelerometer 2.0 plugin

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

from ..tinkerforge.bricklet_accelerometer_v2 import BrickletAccelerometerV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Accelerometer Bricklet 2.0 mit Port D des Master Bricks 3.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Neigung und Drehung müssen zu Bricklet-Position passen
     * LED muss dabei durchgängig blinken
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_acceleration = None
        self.led_is_on = False

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_acceleration != None:
            self.cbe_acceleration.set_period(0)

    def get_device_identifier(self):
        return BrickletAccelerometerV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletAccelerometerV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_acceleration != None:
            self.cbe_acceleration.set_period(0)

        self.accelerometer = BrickletAccelerometerV2(device_information.uid, self.get_ipcon())
        if self.accelerometer.get_bootloader_mode() != BrickletAccelerometerV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_acceleration = CallbackEmulator(self.accelerometer.get_acceleration, self.cb_acceleration)
        self.cbe_acceleration.set_period(100)

        self.show_device_information(device_information)

    def cb_acceleration(self, data):
        if self.led_is_on:
            self.accelerometer.set_info_led_config(0)
        else:
            self.accelerometer.set_info_led_config(1)

        self.led_is_on = not self.led_is_on

        x, y, z = data

        try:
            pitch = int(round(math.atan(x/(math.sqrt(y*y + z*z)))*180/math.pi, 0))
            roll  = int(round(math.atan(y/math.sqrt(x*x+z*z))*180/math.pi, 0))
        except:
            pitch = 0
            roll  = 0

        text = 'Neigungswinkel: {0:+03d}°'.format(pitch)
        text += ', Rollwinkel: {0:+03d}°'.format(roll)
        text = text.replace('-0', '- ')
        text = text.replace('+0', '+ ')
        self.mw.set_value_normal(text)
