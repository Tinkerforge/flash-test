# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

bricklet_industrial_quad_relay_v2_v2.py: Industrial Quad Relay V2 plugin

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

from ..tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Quad Relay V2 Bricklet mit Port D des Master Bricks 3.0
2. Verbinde LED Testadapter mit Industrial Quad Relay V2 Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Alle LEDs müssen blinken (externe und Status-LEDs)
5. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_value = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletIndustrialQuadRelayV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialQuadRelayV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.iqr = BrickletIndustrialQuadRelayV2(device_information.uid, self.get_ipcon())
        if self.iqr.get_bootloader_mode() != BrickletIndustrialQuadRelayV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.iqr.set_value((True, True, True, True))
        self.cbe_value = CallbackEmulator(self.iqr.get_value, self.cb_value)
        self.cbe_value.set_period(500)

        self.show_device_information(device_information)

    def cb_value(self, value):
        self.iqr.set_value((False, False, False, False) if value != (False, False, False, False) else (True, True, True, True))
