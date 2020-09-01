# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2020 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_dual_ac_relay.py: Dual AC Relay plugin

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

from ..tinkerforge.bricklet_industrial_dual_ac_relay import BrickletIndustrialDualACRelay
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Dual AC Relay Bricklet mit Port C
2. Verbinde Testadapter mit Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Beide Relais müssen schalten und die LEDs blinken
6. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
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
        return BrickletIndustrialDualACRelay.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialDualACRelay.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.dr = BrickletIndustrialDualACRelay(device_information.uid, self.get_ipcon())
        if self.dr.get_bootloader_mode() != BrickletIndustrialDualACRelay.BOOTLOADER_MODE_FIRMWARE:
            return

        self.dr.set_value(True, False)
        self.cbe_value = CallbackEmulator(self.dr.get_value, self.cb_value)
        self.cbe_value.set_period(500)

        self.show_device_information(device_information)

    def cb_value(self, value):
        r1, r2 = value
        self.dr.set_value(not r1, not r2)
