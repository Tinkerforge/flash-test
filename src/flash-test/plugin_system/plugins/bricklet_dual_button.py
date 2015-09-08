# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

bricklet_dual_button.py: Dual Button plugin

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

from ..tinkerforge.bricklet_dual_button import BrickletDualButton
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Dual Button Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
4. Überprüfe Taster und LEDs:
     * Tasterdruck schaltet LED an und aus.
     * Tasterdruck wird angezeigt.
5. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    qtcb_state_changed = QtCore.pyqtSignal(int, int, int, int)

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

        self.button_transition = [0, 0] # 0 = not pressed, 1 = pressed, 2 = pressed and released

        self.qtcb_state_changed.connect(self.cb_state_changed)

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletDualButton.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.write_new_uid_to_bricklet()
        self.write_plugin_to_bricklet(get_bricklet_firmware_filename('dual_button'))
        self.master_reset()

    def new_enum(self, device_information):
        self.dual_button = BrickletDualButton(device_information.uid, self.get_ipcon())
        self.dual_button.register_callback(self.dual_button.CALLBACK_STATE_CHANGED, self.qtcb_state_changed.emit)

        self.mw.set_tool_status_okay("Plugin gefunden")

        self.button_transition = [0, 0]
        button_l, button_r = self.dual_button.get_button_state()

        left = 'nicht '
        if button_l != 1:
            left = ''

        right = 'nicht '
        if button_r != 1:
            right = ''

        self.mw.set_value_normal("Links: {0}gedrückt, Rechts: {1}gedrückt, Warte auf Tasterdruck links und rechts".format(left, right))

    def cb_state_changed(self, button_l, button_r, led_l, led_r):
        if self.button_transition[0] == 0 and button_l == 0:
            self.button_transition[0] = 1
        elif self.button_transition[0] == 1 and button_l == 1:
            self.button_transition[0] = 2

        if self.button_transition[1] == 0 and button_r == 0:
            self.button_transition[1] = 1
        elif self.button_transition[1] == 1 and button_r == 1:
            self.button_transition[1] = 2

        left = 'nicht '
        if button_l != 1:
            left = ''

        right = 'nicht '
        if button_r != 1:
            right = ''
            
        set_value = self.mw.set_value_normal
        if self.button_transition == [0, 0]:
            status = 'Warte auf Tasterdruck links und rechts'
        elif self.button_transition == [0, 1]:
            status = 'Warte auf Tasterdruck links und -loslassen rechts'
        elif self.button_transition == [1, 0]:
            status = 'Warte auf Tasterloslassen links und -druck rechts'
        elif self.button_transition == [0, 2]:
            status = 'Warte auf Tasterdruck links'
        elif self.button_transition == [2, 0]:
            status = 'Warte auf Tasterdruck rechts'
        elif self.button_transition == [1, 1]:
            status = 'Warte auf Tasterloslassen links und rechts'
        elif self.button_transition == [1, 2]:
            status = 'Warte auf Tasterloslassen links'
        elif self.button_transition == [2, 1]:
            status = 'Warte auf Tasterloslassen rechts'
        elif self.button_transition == [2, 2]:
            status = 'Test OK!'
            set_value = self.mw.set_value_okay
        else:
            status = 'Logikfehler!' + str(self.button_transition)

        set_value("Links: {0}gedrückt, Rechts: {1}gedrückt, {2}".format(left, right, status))
