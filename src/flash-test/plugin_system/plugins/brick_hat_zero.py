# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

brick_hat_zero_zero.py: HAT plugin

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

from ..tinkerforge.brick_hat_zero import BrickHATZero
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import os

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Nutze neuen flash adapter!!!
1. Verbinde HAT Zero Brick mit flash adapter
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Das HAT Zero Brick muss jetzt mit RPi und RPI-Test-Image getestet werden
5. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_voltage = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

    def get_device_identifier(self):
        return BrickHATZero.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickHATZero.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

        self.hat = BrickHATZero(device_information.uid, self.get_ipcon())
        if self.hat.get_bootloader_mode() != BrickHATZero.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_voltage = CallbackEmulator(self.hat.get_usb_voltage, self.cb_voltage)
        self.cbe_voltage.set_period(100)

        self.show_device_information(device_information)

    def cb_voltage(self, voltage):
        self.mw.set_value_normal('Voltages USB {0:.1f}V'.format(voltage/1000.0))
