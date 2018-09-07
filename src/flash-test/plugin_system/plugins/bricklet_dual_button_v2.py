# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_dual_button_v2.py: Dual Button 2.0 plugin

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

from ..tinkerforge.bricklet_dual_button_v2 import BrickletDualButtonV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Dual Button Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe beide Taster und beide LEDs:
     * Tasterdruck schaltet LED an und aus
     * Tasterdruck wird angezeigt
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    qtcb_state_changed = QtCore.pyqtSignal(int, int, int, int)

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)

        self.button_transition = [0, 0] # 0 = not pressed, 1 = pressed, 2 = pressed and released

        self.qtcb_state_changed.connect(self.cb_state_changed)

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletDualButtonV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletDualButtonV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.dual_button = BrickletDualButtonV2(device_information.uid, self.get_ipcon())
        if self.dual_button.get_bootloader_mode() != BrickletDualButtonV2.BOOTLOADER_MODE_FIRMWARE:
            return
        
        self.dual_button.register_callback(self.dual_button.CALLBACK_STATE_CHANGED, self.qtcb_state_changed.emit)
        self.dual_button.set_state_changed_callback_configuration(True)

        self.show_device_information(device_information)

        self.button_transition = [0, 0]
        button_l, button_r = self.dual_button.get_button_state()

        self.update_button_transition(button_l, button_r)

    def update_button_transition(self, button_l, button_r):
        if self.button_transition[0] == 0 and button_l == self.dual_button.BUTTON_STATE_PRESSED:
            self.button_transition[0] = 1
        elif self.button_transition[0] == 1 and button_l == self.dual_button.BUTTON_STATE_RELEASED:
            self.button_transition[0] = 2

        if self.button_transition[1] == 0 and button_r == self.dual_button.BUTTON_STATE_PRESSED:
            self.button_transition[1] = 1
        elif self.button_transition[1] == 1 and button_r == self.dual_button.BUTTON_STATE_RELEASED:
            self.button_transition[1] = 2

        left = '\u25C7'
        if button_l == self.dual_button.BUTTON_STATE_PRESSED:
            left = '\u25C6'

        right = '\u25C7'
        if button_r == self.dual_button.BUTTON_STATE_PRESSED:
            right = '\u25C6'

        if self.button_transition != [2, 2]:
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

        set_value("Taster: {0} {1}, {2} (\u25C6 = gedrückt, \u25C7 = losgelassen, \u2611 = OK)".format(left, right, status))

    def cb_state_changed(self, button_l, button_r, led_l, led_r):
        self.update_button_transition(button_l, button_r)
