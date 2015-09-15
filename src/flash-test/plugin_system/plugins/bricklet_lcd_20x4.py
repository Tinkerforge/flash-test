# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

bricklet_lcd_20x4.py: LCD 20x4 plugin

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

from ..tinkerforge.bricklet_lcd_20x4 import BrickletLCD20x4
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Stecke LCD auf LCD 20x4 Bricklet
2. Verbinde LCD 20x4 Bricklet mit Port C
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. Stelle Kontrast ein, so dass der Text gut lessbar ist
6. Überprüfe die vier Taster:
     * Tasterdruck wird angezeigt
7. Ziehe LCD von LCD 20x4 Bricklet ab
8. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
9. Gehe zu 1
"""

    qtcb_button_pressed = QtCore.pyqtSignal(int)
    qtcb_button_released = QtCore.pyqtSignal(int)

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

        self.button_transition = [0, 0, 0, 0] # 0 = not pressed, 1 = pressed, 2 = pressed and released

        self.qtcb_button_pressed.connect(self.cb_button_pressed)
        self.qtcb_button_released.connect(self.cb_button_released)

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletLCD20x4.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('lcd_20x4_v12'))

    def new_enum(self, device_information):
        self.lcd = BrickletLCD20x4(device_information.uid, self.get_ipcon())
        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_PRESSED, self.qtcb_button_pressed.emit)
        self.lcd.register_callback(self.lcd.CALLBACK_BUTTON_RELEASED, self.qtcb_button_released.emit)

        self.mw.set_tool_status_okay("Plugin gefunden")

        self.lcd.clear_display()
        self.lcd.backlight_on()
        self.lcd.write_line(0, 0, 'OL')
        self.lcd.write_line(0, 18, 'OR')
        self.lcd.write_line(1, 7, 'Hello')
        self.lcd.write_line(2, 8, 'World')
        self.lcd.write_line(3, 0, 'UL')
        self.lcd.write_line(3, 18, 'UR')

        self.button_transition = [0, 0, 0, 0]

        self.update_button_transition()

    def update_button_transition(self):
        button0 = self.lcd.is_button_pressed(0)
        button1 = self.lcd.is_button_pressed(1)
        button2 = self.lcd.is_button_pressed(2)
        button3 = self.lcd.is_button_pressed(3)

        if self.button_transition[0] == 0 and button0:
            self.button_transition[0] = 1
        elif self.button_transition[0] == 1 and not button0:
            self.button_transition[0] = 2

        if self.button_transition[1] == 0 and button1:
            self.button_transition[1] = 1
        elif self.button_transition[1] == 1 and not button1:
            self.button_transition[1] = 2

        if self.button_transition[2] == 0 and button2:
            self.button_transition[2] = 1
        elif self.button_transition[2] == 1 and not button2:
            self.button_transition[2] = 2

        if self.button_transition[3] == 0 and button3:
            self.button_transition[3] = 1
        elif self.button_transition[3] == 1 and not button3:
            self.button_transition[3] = 2

        s0 = '\u25C7'
        if button0:
            s0 = '\u25C6'

        s1 = '\u25C7'
        if button1:
            s1 = '\u25C6'

        s2 = '\u25C7'
        if button2:
            s2 = '\u25C6'

        s3 = '\u25C7'
        if button3:
            s3 = '\u25C6'

        if self.button_transition != [2, 2, 2, 2]:
            status = 'Warte auf '
            set_value = self.mw.set_value_action

            for bs in self.button_transition:
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

        set_value("Taster: {0} {1} {2} {3}, {4} (\u25C6 = gedrückt, \u25C7 = losgelassen, \u2611 = OK)".format(s0, s1, s2, s3, status))

    def cb_button_pressed(self, button):
        self.update_button_transition()

    def cb_button_released(self, button):
        self.update_button_transition()
