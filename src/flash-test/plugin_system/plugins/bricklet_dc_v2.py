# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2021 Olaf Lüke <olaf@tinkerforge.com>

bricklet_dc_v2.py: DC 2.0 plugin

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

from ..tinkerforge.bricklet_dc_v2 import BrickletDCV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math
import time

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
Pre-Flash/Test: Kühlkörper aufkleben!

0. Baue Netzteil auf, verbinde Motor mit Netzteil und stelle Spannung auf 10V.
1. Stecke Motor (mit grünem und schwarzem Stecker) in DC Bricklet 2.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe ob Motor sich dreht (3 Sekunden Beschleunigung mit anschließender Debeschleunigung)
5. Das Brick ist fertig, mit schwarzem und grünen 2-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_power_statistics = None
        self.led_is_on = False

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_power_statistics != None:
            self.cbe_power_statistics.set_period(0)

    def get_device_identifier(self):
        return BrickletDCV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletDCV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_power_statistics != None:
            self.cbe_power_statistics.set_period(0)

        self.dc = BrickletDCV2(device_information.uid, self.get_ipcon())
        if self.dc.get_bootloader_mode() != BrickletDCV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.show_device_information(device_information)
        self.cbe_power_statistics = CallbackEmulator(self.dc.get_power_statistics, self.cb_power_statistics)
        self.cbe_power_statistics.set_period(100)

        self.start_time = 0

    def cb_power_statistics(self, data):
        if self.start_time == 0:
            self.dc.set_pwm_frequency(10000)
            self.dc.set_drive_mode(0)
            self.dc.set_enabled(True)
            self.dc.set_motion(10000, 10000)
            self.dc.set_velocity(32767)
            self.start_time = time.time()
        elif time.time() - self.start_time > 3:
            self.dc.set_velocity(0)
            self.dc.set_enabled(False)

        self.mw.set_value_normal('Voltage: {0:.2f}V, Current: {1:.2f}A'.format(data.voltage/1000, data.current/1000))
