# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_oled_128x64_v2.py: OLED 128x64 2.0 plugin

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

from ..tinkerforge.bricklet_oled_128x64_v2 import BrickletOLED128x64V2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

STATE_VERTICAL = 0
STATE_HORIZONTAL = 1
STATE_ALL_ON = 2

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde OLED 128x64 Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Streifen wandert auf Display Vertikal und Horizontal
5. Bildschirm wird vollflächig weiß, auf Pixelfehler prüfen
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.state = STATE_VERTICAL
        self.num = 0
        self.cbe_state = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_state != None:
            self.cbe_state.set_period(0)

    def get_device_identifier(self):
        return BrickletOLED128x64V2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletOLED128x64V2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_state != None:
            self.cbe_state.set_period(0)

        self.oled = BrickletOLED128x64V2(device_information.uid, self.get_ipcon())
        if self.oled.get_bootloader_mode() != BrickletOLED128x64V2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.oled.set_display_configuration(143, False, False)
        self.oled.clear_display()
        self.cbe_state = CallbackEmulator(self.oled.get_display_configuration, self.cb_state, ignore_last_data=True)
        self.cbe_state.set_period(25)
        self.show_device_information(device_information)

    def cb_state(self, _):
        if self.state == STATE_VERTICAL:
            data = [True]*128
            self.oled.write_pixels(0, self.num, 127, self.num, data)
            self.oled.draw_buffered_frame(False)
            data = [False]*128
            self.oled.write_pixels(0, self.num, 127, self.num, data)
        elif self.state == STATE_HORIZONTAL:
            data = [True]*64
            self.oled.write_pixels(self.num, 0, self.num, 63, data)
            self.oled.draw_buffered_frame(False)
            data = [False]*64
            self.oled.write_pixels(self.num, 0, self.num, 63, data)
        else:
            if self.num == 0:
                data = [True]*64*128
                self.oled.write_pixels(0, 0, 127, 63, data)
                self.oled.draw_buffered_frame(False)
            elif self.num == 3000/25 - 1:
                data = [False]*64*128
                self.oled.write_pixels(0, 0, 127, 63, data)
                self.oled.draw_buffered_frame(False)

        self.num += 1

        if self.state == STATE_VERTICAL:
            if self.num >= 63:
                self.num = 0
                self.state = STATE_HORIZONTAL
        elif self.state == STATE_HORIZONTAL:
            if self.num >= 127:
                self.num = 0
                self.state = STATE_ALL_ON
        else:
            if self.num >= 3000/25:
                self.num = 0
                self.state = STATE_VERTICAL
