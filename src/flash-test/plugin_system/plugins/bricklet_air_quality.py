# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_air_quality.py: Air Quality plugin

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

from ..tinkerforge.bricklet_air_quality import BrickletAirQuality
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde AirQuality Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * IAQ Index egal
     * Temperatur zwischen 20 und 30
     * Luftfeuchte zwischen 30 und 70
     * Luftdruck zwischen 950 und 1050
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_all_values = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_all_values != None:
            self.cbe_all_values.set_period(0)

    def get_device_identifier(self):
        return BrickletAirQuality.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletAirQuality.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_all_values != None:
            self.cbe_all_values.set_period(0)

        self.air_quality = BrickletAirQuality(device_information.uid, self.get_ipcon())
        if self.air_quality.get_bootloader_mode() != BrickletAirQuality.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_all_values = CallbackEmulator(self.air_quality.get_all_values, self.cb_all_values)
        self.cbe_all_values.set_period(100)

        self.show_device_information(device_information)

    def cb_all_values(self, values):
        iaq_index, iaq_index_accuracy, temperature, humidity, air_pressure = values

        if (950 < air_pressure/100.0 < 1050) and (30 < humidity/100.0 < 70) and (20 < temperature/100.0 < 30):
            set_value = self.mw.set_value_okay
        else:
            set_value = self.mw.set_value_error

        set_value('IAQ Index {0} (Acc {1})\nTemperatur {2} °C\nLuftfeuchte {3} %\nLuftdruck {4} mbar'.format(iaq_index, iaq_index_accuracy, temperature//100, humidity//100, air_pressure//100))
