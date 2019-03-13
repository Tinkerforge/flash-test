# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_digital_out_4_v2.py: Industrial Digital Out 4 2.0 plugin

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

from ..tinkerforge.bricklet_industrial_digital_out_4_v2 import BrickletIndustrialDigitalOut4V2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Digital Out 4 Bricklet 2.0 mit Port C
2. Verbinde LED-Testadapter mit Industrial Digital Out 4 Bricklet 2.0
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Alle LEDs müssen blinken
6. Überprüfe Kanal-LEDs
7. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_value = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletIndustrialDigitalOut4V2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialDigitalOut4V2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.ido4 = BrickletIndustrialDigitalOut4V2(device_information.uid, self.get_ipcon())
        if self.ido4.get_bootloader_mode() != BrickletIndustrialDigitalOut4V2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.ido4.set_value((True, True, True, True))
        self.cbe_value = CallbackEmulator(self.ido4.get_value, self.cb_value)
        self.cbe_value.set_period(500)

        self.show_device_information(device_information)

    def cb_value(self, value):
        self.ido4.set_value((False, False, False, False) if value[0] else (True, True, True, True))
