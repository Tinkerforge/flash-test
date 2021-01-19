# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_performance_dc.py: Performance DC plugin

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

from ..tinkerforge.bricklet_performance_dc import BrickletPerformanceDC
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Stromversorgung, Motor und GPIO-Tester anschließen
1. Verbinde Performance DC Bricklet mit Port D
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Motor fährt abwechselnd vorwärts/rückwärts
     * Überprüfe CW / CCW LED leuchtet
5. Überprüfe beide Taster und beide GPIO LEDs:
     * Tasterdruck schaltet LED an und aus
     * Tasterdruck wird angezeigt
6. Überprüfe Error LED (heartbeat)
7. Das Bricklet ist fertig, Kühllörper aufkleben, in ESD-Tüte stecken inklusive drei Stecker, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.gpio_state = None
        self.count = 0

        self.gpio_transition = [0, 0] # 0 = not pressed, 1 = pressed, 2 = pressed and released

    def start(self):
        CoMCUBrickletBase.start(self)
        self.count = 0

    def stop(self):
        super().stop()
        self.count = 0
        if self.gpio_state != None:
            self.gpio_state.set_period(0)

    def get_device_identifier(self):
        return BrickletPerformanceDC.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletPerformanceDC.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.gpio_state != None:
            self.gpio_state.set_period(0)

        self.pdc = BrickletPerformanceDC(device_information.uid, self.get_ipcon())
        if self.pdc.get_bootloader_mode() != BrickletPerformanceDC.BOOTLOADER_MODE_FIRMWARE:
            return

        self.gpio_state = CallbackEmulator(self.pdc.get_gpio_state, self.cb_gpio_state, ignore_last_data=True)
        self.gpio_state.set_period(10)

        self.show_device_information(device_information)

        self.pdc.set_error_led_config(self.pdc.ERROR_LED_CONFIG_SHOW_HEARTBEAT)
        self.pdc.set_enabled(True)
        self.pdc.set_velocity(5000)
        self.count = 0

        self.gpio_transition = [0, 0]
        gpio0, gpio1 = self.pdc.get_gpio_state()

        self.update_gpio_transition(gpio0, gpio1)

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

        set_value("Taster: {0} {1}, {2} (\u25C6 = gedrückt, \u25C7 = losgelassen, \u2611 = OK)".format(left, right, status))

    def cb_gpio_state(self, state):
        self.update_gpio_transition(*state)

        self.count += 1
        if self.count >= 100:
            self.count = 0
            self.pdc.set_velocity(-self.pdc.get_velocity())

