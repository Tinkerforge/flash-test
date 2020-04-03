# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_gps_v2.py: GPS 2.0 plugin

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

import datetime

from PyQt5 import Qt, QtGui, QtCore

from ..tinkerforge.bricklet_gps_v2 import BrickletGPSV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Antenne aufkleben
1. Verbinde GPS 2.0 Bricklet mit Flash Adapter XMC
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
    * Wert entspricht einer Zeit und sollte sich 1x pro Sekunde erhöhen
5. Das Bricklet ist fertig, zusammen mit Batterie in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_datetime = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_datetime != None:
            self.cbe_datetime.set_period(0)

    def get_device_identifier(self):
        return BrickletGPSV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletGPSV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.gps = BrickletGPSV2(device_information.uid, self.get_ipcon())
        if self.gps.get_bootloader_mode() != BrickletGPSV2.BOOTLOADER_MODE_FIRMWARE:
            return

        if self.cbe_datetime != None:
            self.cbe_datetime.set_period(0)

        self.cbe_datetime = CallbackEmulator(self.gps.get_date_time, self.cb_datetime)
        self.cbe_datetime.set_period(100)

        self.show_device_information(device_information)

    def cb_datetime(self, ret):
        date = ret.date
        time = ret.time
        yy = date % 100
        yy += 2000
        date //= 100
        mm = date % 100
        date //= 100
        dd = date

        us = (time % 1000) * 1000
        time //= 1000
        ss = time % 100
        time //= 100
        mins = time % 100
        time //= 100
        hh = time

        try:
            date_str = datetime.datetime(yy, mm, dd, hh, mins, ss, us).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + " UTC"
        except Exception as e:
            date_str = "Unknown: " + str(e)
        self.mw.set_value_normal(date_str)
