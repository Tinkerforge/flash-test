# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_joystick_v2.py: Joystick 2.0 plugin

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

from PyQt5.QtCore import pyqtSignal

from ..tinkerforge.bricklet_joystick_v2 import BrickletJoystickV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

LIMIT = 99

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Joystick Bricklet 2.0 mit Port D des Master Bricks 3.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Joystick und Taster:
     * Joystick wird in allen vier Ecken erkannt
     * Tasterdruck wird angezeigt
5. Das Bricklet ist fertig, mit einem Joystick-Knopf in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    qtcb_pressed = pyqtSignal(bool)

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)

        self.cbe_position = None
        self.position_transition = [0, 0, 0, 0] # [TR, BR, BL, TL] 0 = not arrived, 1 = arrived, 2 = arrived and left
        self.button_transition = 0 # 0 = not pressed, 1 = pressed, 2 = pressed and released
        self.last_position_status = '?', '?', '?', '?'
        self.last_button_status = '?'

        self.qtcb_pressed.connect(self.cb_button)

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_position != None:
            self.cbe_position.set_period(0)

    def get_device_identifier(self):
        return BrickletJoystickV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletJoystickV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_position != None:
            self.cbe_position.set_period(0)

        self.joystick = BrickletJoystickV2(device_information.uid, self.get_ipcon())
        if self.joystick.get_bootloader_mode() != BrickletJoystickV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.joystick.register_callback(self.joystick.CALLBACK_PRESSED, self.qtcb_pressed.emit)
        self.joystick.set_pressed_callback_configuration(10, True)

        self.cbe_position = CallbackEmulator(self.joystick.get_position, self.cb_position)
        self.cbe_position.set_period(100)

        self.show_device_information(device_information)

        self.position_transition = [0, 0, 0, 0]
        self.button_transition = 0
        self.last_position_status = '?', '?', '?', '?'
        self.last_button_status = '?'
        self.last_position = 0, 0

        x, y = self.joystick.get_position()
        pressed = self.joystick.is_pressed()

        self.update_transition(x, y, pressed)

    def update_transition(self, x, y, pressed):
        if x != None and y != None:
            # TR
            if self.position_transition[0] == 0 and x >= LIMIT and y >= LIMIT:
                self.position_transition[0] = 1
            elif self.position_transition[0] == 1 and not (x >= LIMIT and y >= LIMIT):
                self.position_transition[0] = 2

            # BR
            if self.position_transition[1] == 0 and x >= LIMIT and y <= -LIMIT:
                self.position_transition[1] = 1
            elif self.position_transition[1] == 1 and not (x >= LIMIT and y <= -LIMIT):
                self.position_transition[1] = 2

            # BL
            if self.position_transition[2] == 0 and x <= -LIMIT and y <= -LIMIT:
                self.position_transition[2] = 1
            elif self.position_transition[2] == 1 and not (x <= -LIMIT and y <= -LIMIT):
                self.position_transition[2] = 2

            # TL
            if self.position_transition[3] == 0 and x <= -LIMIT and y >= LIMIT:
                self.position_transition[3] = 1
            elif self.position_transition[3] == 1 and not (x <= -LIMIT and y >= LIMIT):
                self.position_transition[3] = 2

        if pressed != None:
            if self.button_transition == 0 and pressed:
                self.button_transition = 1
            elif self.button_transition == 1 and not pressed:
                self.button_transition = 2

        if x != None and y != None:
            tr = '\u25C7'
            if x >= LIMIT and y >= LIMIT:
                tr = '\u25C6'

            br = '\u25C7'
            if x >= LIMIT and y <= -LIMIT:
                br = '\u25C6'

            bl = '\u25C7'
            if x <= -LIMIT and y <= -LIMIT:
                bl = '\u25C6'

            tl = '\u25C7'
            if x <= -LIMIT and y >= LIMIT:
                tl = '\u25C6'

            self.last_position_status = tr, br, bl, tl
        else:
            tr, br, bl, tl = self.last_position_status

        if pressed != None:
            bs = '\u25C7'
            if pressed:
                bs = '\u25C6'

            self.last_button_status = bs
        else:
            bs = self.last_button_status

        if self.position_transition != [2, 2, 2, 2] or self.button_transition != 2:
            status = 'Warte auf '
            set_value = self.mw.set_value_action

            for ps in self.position_transition:
                if ps == 0:
                    status += '\u25C6 '
                elif ps == 1:
                    status += '\u25C7 '
                elif ps == 2:
                    status += '\u2611 '
                else:
                    status += '? '

            status += 'und '

            if self.button_transition == 0:
                status += '\u25C6'
            elif self.button_transition == 1:
                status += '\u25C7'
            elif self.button_transition == 2:
                status += '\u2611'
            else:
                status += str(self.button_transition)
        else:
            status = 'Test OK!'
            set_value = self.mw.set_value_okay

        if x != None and y != None:
            self.last_position = x, y
        else:
            x, y = self.last_position

        set_value("Position: ({0}, {1})\nEcken und Taster: {2} {3} {4} {5} und {6}, {7} (\u25C6 = drin/gedrückt, \u25C7 = draußen/losgelassen, \u2611 = OK)"
                  .format(x, y, tr, br, bl, tl, bs, status))

    def cb_position(self, data):
        x, y = data
        self.update_transition(x, y, None)

    def cb_button(self, pressed):
        self.update_transition(None, None, pressed)
