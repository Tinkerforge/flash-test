# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_barometer_v2.py: BarometerV2 plugin

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

from ..tinkerforge.bricklet_barometer_v2 import BrickletBarometerV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Barometer 2.0 Bricklet mit Port D des Master Bricks 3.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Wert sollte zwischen ~950 und ~1050 liegen
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_air_pressure = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_air_pressure != None:
            self.cbe_air_pressure.set_period(0)

    def get_device_identifier(self):
        return BrickletBarometerV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletBarometerV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_air_pressure != None:
            self.cbe_air_pressure.set_period(0)

        self.b = BrickletBarometerV2(device_information.uid, self.get_ipcon())
        if self.b.get_bootloader_mode() != BrickletBarometerV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_air_pressure = CallbackEmulator(self.b.get_air_pressure, self.cb_air_pressure)
        self.cbe_air_pressure.set_period(100)

        self.show_device_information(device_information)

    def cb_air_pressure(self, air_pressure):
        if (950 < air_pressure/1000.0 < 1050):
            set_value = self.mw.set_value_okay
        else:
            set_value = self.mw.set_value_error

        set_value('{0:.3f} mbar'.format(air_pressure/1000.0).replace('.', ','))
