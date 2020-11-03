# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

bricklet_servo_v2.py: Servo 2.0 plugin

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

from ..tinkerforge.bricklet_servo_v2 import BrickletServoV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Stecke schwarzen Stecker in Servo Bricklet 2.0, Stecke Servo an Position 0 (schwarz unten)
1. Verbinde Servo Bricklet 2.0 mit Flash Adapter XMC
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe ob Servo sich dreht (Mittelposition, +90°, -90°)
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_servo_current = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_servo_current != None:
            self.cbe_servo_current.set_period(0)

    def get_device_identifier(self):
        return BrickletServoV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletServoV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        print(device_information)
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_servo_current != None:
            self.cbe_servo_current.set_period(0)

        self.servo = BrickletServoV2(device_information.uid, self.get_ipcon())
        if self.servo.get_bootloader_mode() != BrickletServoV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.state = 0
        self.servo.set_enable(0, True)
        self.servo.set_motion_configuration(0, 0xFFFF, 0xFFFF, 0xFFFF)
        self.cbe_servo_current = CallbackEmulator(lambda: self.servo.get_servo_current(0), self.cb_servo_current, ignore_last_data=True)
        self.cbe_servo_current.set_period(500)

        self.show_device_information(device_information)

    def cb_servo_current(self, current):
        print(current)

        if self.state == 0:
            self.servo.set_position(0, 0)
        elif self.state == 1:
            self.servo.set_position(0, 9000)
        elif self.state == 2:
            self.servo.set_position(0, -9000)

        self.state = (self.state + 1) % 3

        voltage = self.servo.get_input_voltage()

        self.mw.set_value_normal('Current: {0}mA, Input Voltage: {1:.2f}V'.format(current, voltage/1000))
