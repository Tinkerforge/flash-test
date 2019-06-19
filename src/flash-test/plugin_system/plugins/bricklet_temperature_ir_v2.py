# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_temperature_ir_v2.py: Temperature IR plugin

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

from ..tinkerforge.bricklet_temperature_ir_v2 import BrickletTemperatureIRV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Temperature IR Bricklet mit 2.0 Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert: Temperatur sollte passen
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_temperature = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_temperature != None:
            self.cbe_temperature.set_period(0)

    def get_device_identifier(self):
        return BrickletTemperatureIRV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletTemperatureIRV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_temperature != None:
            self.cbe_temperature.set_period(0)

        self.temp_ir = BrickletTemperatureIRV2(device_information.uid, self.get_ipcon())
        if self.temp_ir.get_bootloader_mode() != BrickletTemperatureIRV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_temperature = CallbackEmulator(self.temp_ir.get_object_temperature,
                                                self.cb_temperature)
        self.cbe_temperature.set_period(100)

        self.show_device_information(device_information)

    def cb_temperature(self, object_temperature):
        ambient_temperature =  self.temp_ir.get_ambient_temperature()
        if (100 < ambient_temperature < 300) and (100 < object_temperature < 300):
            set_value = self.mw.set_value_okay
        else:
            set_value = self.mw.set_value_error

        set_value('Objekt: ' + str(object_temperature//10) + ' °C, Umgebung: ' + str(ambient_temperature//10) + ' °C')
