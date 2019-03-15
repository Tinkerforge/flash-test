# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_rgb_led_v2.py: RGB LED 2.0 plugin

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

from ..tinkerforge.bricklet_rgb_led_v2 import BrickletRGBLEDV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde RGB LED Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. LED ändert Farbe: R -> G -> B -> W
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_rgb_value = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_rgb_value != None:
            self.cbe_rgb_value.set_period(0)

    def get_device_identifier(self):
        return BrickletRGBLEDV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletRGBLEDV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_rgb_value != None:
            self.cbe_rgb_value.set_period(0)

        self.rgb_led = BrickletRGBLEDV2(device_information.uid, self.get_ipcon())
        if self.rgb_led.get_bootloader_mode() != BrickletRGBLEDV2.BOOTLOADER_MODE_FIRMWARE:
            return
        self.cbe_rgb_value = CallbackEmulator(self.rgb_led.get_rgb_value, self.cb_rgb_value)
        self.cbe_rgb_value.set_period(500)

        self.show_device_information(device_information)

    def cb_rgb_value(self, value):
        r = value.r
        g = value.g
        b = value.b

        r_new = 0
        g_new = 0
        b_new = 0

        if r == 255 and g == 255 and b == 255:
            r_new = 255
            g_new = 0
            b_new = 0
        elif r == 255:
            r_new = 0
            g_new = 255
            b_new = 0
        elif g == 255:
            r_new = 0
            g_new = 0
            b_new = 255
        else:
            r_new = 255
            g_new = 255
            b_new = 255

        self.rgb_led.set_rgb_value(r_new, g_new, b_new)
