# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_outdoor_weather.py: Outdoor Weather plugin

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

from ..tinkerforge.bricklet_outdoor_weather import BrickletOutdoorWeather
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Verbinde Outdoor Weather Bricklet mit Port C
1. Schließe Antenna an Bricklet an
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Werte (Wetterstation sendet Werte alle ~60 Sekunden)
5. Das Bricklet ist fertig, mit Antenne in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_station_identifiers = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_station_identifiers != None:
            self.cbe_station_identifiers.set_period(0)

    def get_device_identifier(self):
        return BrickletOutdoorWeather.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletOutdoorWeather.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_station_identifiers != None:
            self.cbe_station_identifiers.set_period(0)

        self.ow = BrickletOutdoorWeather(device_information.uid, self.get_ipcon())
        if self.ow.get_bootloader_mode() != BrickletOutdoorWeather.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_station_identifiers = CallbackEmulator(self.ow.get_station_identifiers,
                                             self.cb_station_identifiers)
        self.cbe_station_identifiers.set_period(500)

        self.show_device_information(device_information)

    def cb_station_identifiers(self, ids):
        if len(ids) == 0:
            return

        data = self.ow.get_station_data(ids[0])
        try:
            wind_direction = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW'][data.wind_direction]
        except:
            wind_direction = 'Unbekannt (Error)'

        text = ''
        text += "Temperatur: {:.1f}\n".format(data.temperature/10.0)
        text += "Luftfeuchte: {:.1f}\n".format(data.humidity)
        text += "Wind Geschwindigkeit: {:.1f}\n".format(data.wind_speed/10.0)
        text += "Böhen Geschwindigkeit: {:.1f}\n".format(data.gust_speed/10.0)
        text += "Regenlevel: {:.1f}\n".format(data.rain)
        text += "Windrichtung: {}\n".format(wind_direction)
        if data.battery_low:
            text += "Batterie: Leer\n"
        else:
            text += "Batterie: Voll\n"

        self.mw.set_value_normal(text)
