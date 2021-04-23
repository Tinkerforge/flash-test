# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2021 Olaf Lüke <olaf@tinkerforge.com>

bricklet_silent_stepper_v2.py: Silent Stepper 2.0 plugin

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

from PyQt5 import Qt, QtGui, QtCore, QtWidgets

from ..tinkerforge.bricklet_silent_stepper_v2 import BrickletSilentStepperV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math
import time

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
Pre-Flash/Test: Kühlkörper aufkleben!

1. Stecke schwarzen Stecker (24V) und grünen Stecker (Motor) und GPIO-Tester in Silent Stepper Bricklet 2.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe ob Schrittmotor sich abwechselnd in beide Richtungen dreht
5. Überprüfe Spannungswert:
    * Externe Versorgungsspannung sollte um die 24V liegen
6. Überprüfe beide Taster:
    * Tastendruck wird angezeigt
7. Kühlkörper auf Silent Stepper Brick aufkleben
8. Das Bricklet ist fertig, mit schwarzem 2-Pol Stecker und grünem 4-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
9. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_input_voltage = None
        self.gpio_transition = [0, 0] # 0 = not pressed, 1 = pressed, 2 = pressed and release

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_input_voltage != None:
            self.cbe_input_voltage.set_period(0)

    def get_device_identifier(self):
        return BrickletSilentStepperV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletSilentStepperV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_input_voltage != None:
            self.cbe_input_voltage.set_period(0)

        self.silent_stepper = BrickletSilentStepperV2(device_information.uid, self.get_ipcon())
        if self.silent_stepper.get_bootloader_mode() != BrickletSilentStepperV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.show_device_information(device_information)
        self.cbe_input_voltage = CallbackEmulator(self.silent_stepper.get_input_voltage, self.cb_input_voltage)
        self.cbe_input_voltage.set_period(100)

        self.gpio_transition = [0, 0]
        gpio_state = self.silent_stepper.get_gpio_state()
        self.update_gpio_transition(*gpio_state)

        QtWidgets.QApplication.processEvents()

        self.silent_stepper.set_motor_current(800)
        self.silent_stepper.set_step_configuration(BrickletSilentStepperV2.STEP_RESOLUTION_1, 1)
        self.silent_stepper.set_max_velocity(1000)
        self.silent_stepper.set_speed_ramping(20000, 20000)
        self.silent_stepper.set_enabled(True)
        self.silent_stepper.drive_forward()
        time.sleep(0.75)
        QtWidgets.QApplication.processEvents()
        self.silent_stepper.stop()
        time.sleep(0.25)
        QtWidgets.QApplication.processEvents()
        self.silent_stepper.drive_backward()
        time.sleep(0.75)
        QtWidgets.QApplication.processEvents()
        self.silent_stepper.stop()
        time.sleep(0.25)
        QtWidgets.QApplication.processEvents()
        self.silent_stepper.set_enabled(False)


    # transition function taken from dual button plugin
    def update_gpio_transition(self, gpio0, gpio1):
        if self.gpio_transition[0] == 0 and gpio0 == True:
            self.gpio_transition[0] = 1
        elif self.gpio_transition[0] == 1 and gpio0 == False:
            self.gpio_transition[0] = 2

        if self.gpio_transition[1] == 0 and gpio1 == True:
            self.gpio_transition[1] = 1
        elif self.gpio_transition[1] == 1 and gpio1 == False:
            self.gpio_transition[1] = 2

        left = '\u25C7'
        if gpio0 == True:
            left = '\u25C6'

        right = '\u25C7'
        if gpio1 == True:
            right = '\u25C6'

        if self.gpio_transition != [2, 2]:
            status = 'Warte auf '
            set_value = self.mw.set_value_action

            for bs in self.gpio_transition:
                if bs == 0:
                    status += '\u25C6 '
                elif bs == 1:
                    status += '\u25C7 '
                elif bs == 2:
                    status += '\u2611 '
                else:
                    status += '? '
        else:
            status = 'Test OK!'
            set_value = self.mw.set_value_okay

        return set_value, "Taster: {0} {1}, {2} (\u25C6 = gedrückt, \u25C7 = losgelassen, \u2611 = OK)".format(left, right, status)


    def cb_input_voltage(self, voltage):
        gpio_state = self.silent_stepper.get_gpio_state()
        print_func, gpio_str = self.update_gpio_transition(*gpio_state)
        print_func('{0}\n\nVoltage: {1:.2f}V'.format(gpio_str, voltage/1000))
