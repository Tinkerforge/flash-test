# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_led_strip_v2.py: LED Strip 2.0 plugin

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

from ..tinkerforge.bricklet_led_strip_v2 import BrickletLEDStripV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Drücke LED Strip Bricklet Tester auf LED Strip Bricklet 2.0
2. Verbinde LED Strip Bricklet 2.0 mit Port C
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. LED ändert Farbe: R -> G -> B -> W
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_led_values = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_led_values != None:
            self.cbe_led_values.set_period(0)

    def get_device_identifier(self):
        return BrickletLEDStripV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletLEDStripV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_led_values != None:
            self.cbe_led_values.set_period(0)

        self.led_strip_v2 = BrickletLEDStripV2(device_information.uid, self.get_ipcon())
        if self.led_strip_v2.get_bootloader_mode() != BrickletLEDStripV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.led_strip_v2.set_chip_type(BrickletLEDStripV2.CHIP_TYPE_WS2801)
        self.led_strip_v2.set_led_values(0, [255, 0, 0])
        self.cbe_led_values = CallbackEmulator(lambda: self.led_strip_v2.get_led_values(0, 3), self.cb_led_values, ignore_last_data=True)
        self.cbe_led_values.set_period(250)

        self.show_device_information(device_information)

    def cb_led_values(self, values):
        r = values[0]
        g = values[1]
        b = values[2]

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

        self.led_strip_v2.set_led_values(0, [r_new, g_new, b_new])
