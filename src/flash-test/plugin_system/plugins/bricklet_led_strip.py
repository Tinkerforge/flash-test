# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_led_strip.py: LED Strip plugin

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

from ..tinkerforge.bricklet_led_strip import BrickletLEDStrip
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Drücke LED Strip Bricklet Tester auf LED Strip Bricklet
2. Verbinde LED Strip Bricklet mit Port C
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. LED ändert Farbe: R -> G -> B -> W 
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_rgb_values = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_rgb_values != None:
            self.cbe_rgb_values.set_period(0)

    def get_device_identifier(self):
        return BrickletLEDStrip.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('led_strip'))

    def new_enum(self, device_information):
        if self.cbe_rgb_values != None:
            self.cbe_rgb_values.set_period(0)

        self.led_strip = BrickletLEDStrip(device_information.uid, self.get_ipcon())
        self.led_strip.set_chip_type(BrickletLEDStrip.CHIP_TYPE_WS2811)
        self.cbe_rgb_values = CallbackEmulator(lambda: self.led_strip.get_rgb_values(0, 1), self.cb_rgb_values)
        self.cbe_rgb_values.set_period(250)

        self.show_device_information(device_information)

    def cb_rgb_values(self, values):
        r = values.r[0]
        g = values.g[0]
        b = values.b[0]
        
        r_new = [0]*16
        g_new = [0]*16
        b_new = [0]*16
        
        if r == 255 and g == 255 and b == 255:
            r_new[0] = 255
            g_new[0] = 0
            b_new[0] = 0
        elif r == 255:
            r_new[0] = 0
            g_new[0] = 255
            b_new[0] = 0
        elif g == 255:
            r_new[0] = 0
            g_new[0] = 0
            b_new[0] = 255
        else:
            r_new[0] = 255
            g_new[0] = 255
            b_new[0] = 255
        
        self.led_strip.set_rgb_values(0, 1, r_new, g_new, b_new)
