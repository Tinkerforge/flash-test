# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_rgb_led_button.py: RGB LED Button plugin

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

from ..tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde RGB LED Button mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Knopf drücken uns loslassen
5. Überprüfe:
     * Wert wechselt von "Losgelassen" auf "Gedrückt" auf "Losgelassen" und wird grün
     * Farbe der LED wechselt zwischen rot, grün, blau, weiß, aus
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_button_state = None
        self.state_seen = True
        self.state_seen_counter = 0
        self.color = 0

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_button_state != None:
            self.cbe_button_state.set_period(0)

    def get_device_identifier(self):
        return BrickletRGBLEDButton.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletRGBLEDButton.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.mw.set_value_normal('Warte auf Knopfdrück')
        self.state_seen_counter = 0

        if self.cbe_button_state != None:
            self.cbe_button_state.set_period(0)

        self.button = BrickletRGBLEDButton(device_information.uid, self.get_ipcon())
        if self.button.get_bootloader_mode() != BrickletRGBLEDButton.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_button_state = CallbackEmulator(self.button.get_button_state,
                                                 self.cb_button_state,
                                                 ignore_last_data=True)
        self.cbe_button_state.set_period(50)

        self.show_device_information(device_information)

    def cb_button_state(self, button_state):
        if button_state != self.state_seen:
            self.state_seen = button_state
            self.state_seen_counter += 1

        set_value = self.mw.set_value_normal
        if self.state_seen_counter > 1:
            set_value = self.mw.set_value_okay

        if button_state:
            set_value('Losgelassen')
        else:
            set_value('Gedrückt')

        if self.color < 10:
            self.button.set_color(255, 0 , 0)
        elif self.color < 20:
            self.button.set_color(0, 255 , 0)
        elif self.color < 30:
            self.button.set_color(0, 0 , 255)
        elif self.color < 40:
            self.button.set_color(255, 255 , 255)
        else:
            self.button.set_color(0, 0 , 0)

        self.color = (self.color + 1) % 50
