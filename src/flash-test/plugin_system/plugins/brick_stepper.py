# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <olaf@tinkerforge.com>

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

from PyQt5 import Qt, QtWidgets, QtCore

from ..tinkerforge.brick_stepper import BrickStepper
from ..brick_base import BrickBase, get_brick_firmware_filename
from ..callback_emulator import CallbackEmulator

import time

class Plugin(BrickBase):
    TODO_TEXT = u"""\
1. Stecke schwarzen Stecker (24V) und grünen Stecker (Motor) in Stepper Brick
2. Verbinde Stepper Brick mit PC per Mini-USB
3. Falls Brick nicht geflasht wird, drücke "Erase"- und "Reset"-Taster
4. Überprüfe ob Schrittmotor sich abwechselnd in beide Richtungen dreht
5. Überprüfe Wert:
    * Externe Versorgungsspannung sollte um die 24V liegen
6. Kühlkörper auf Stepper Brick aufkleben
7. Das Bricklet ist fertig, mit schwarzem 2-Pol Stecker und grünem 4-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben*
8. Gehe zu 1

* Es muss zusätzlich noch ein Stapeltest mit 1x Master Brick, 8x Stepper Brick und 2x Extension gemacht werden.
"""
    FIRMWARE_FILENAME = get_brick_firmware_filename(BrickStepper.DEVICE_URL_PART)

    def __init__(self, *args):
        BrickBase.__init__(self, *args)
        self.cbe_voltage = None

    def start(self, device_information):
        BrickBase.start(self, device_information)

    def stop(self):
        super().stop()
        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

    def get_device_identifier(self):
        return BrickStepper.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

        self.show_device_information(device_information)

        stepper = BrickStepper(device_information.uid, self.get_ipcon())
        self.cbe_voltage = CallbackEmulator(stepper.get_external_input_voltage,
                                            self.cb_voltage)
        self.cbe_voltage.set_period(100)
        self.cb_voltage(stepper.get_external_input_voltage())
        QtWidgets.QApplication.processEvents()

        stepper.set_motor_current(1200)
        stepper.set_step_mode(8)
        stepper.set_max_velocity(5000)
        stepper.set_speed_ramping(20000, 20000)
        stepper.enable()
        stepper.drive_forward()
        time.sleep(0.75)
        QtWidgets.QApplication.processEvents()
        stepper.stop()
        time.sleep(0.25)
        QtWidgets.QApplication.processEvents()
        stepper.drive_backward()
        time.sleep(0.75)
        QtWidgets.QApplication.processEvents()
        stepper.stop()
        time.sleep(0.25)
        QtWidgets.QApplication.processEvents()
        stepper.disable()

    def cb_voltage(self, voltage):
        self.mw.set_value_normal("Externe Versorgungsspannung: " + str(round(voltage/1000.0, 2)) + ' V')
