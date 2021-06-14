# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2020 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_ptc.py: Industrial PTC plugin

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

from ..tinkerforge.bricklet_industrial_ptc import BrickletIndustrialPTC
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Verbinde Industrial PTC Bricklet mit Port D des Master Bricks 3.0
1. Pt100 anstecken und Dippschalter auf Pt100/2-Leiter
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Temperatur sollte sinnvoll sein
6. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
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
        return BrickletIndustrialPTC.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialPTC.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_temperature != None:
            self.cbe_temperature.set_period(0)

        self.industrial_ptc = BrickletIndustrialPTC(device_information.uid, self.get_ipcon())
        if self.industrial_ptc.get_bootloader_mode() != BrickletIndustrialPTC.BOOTLOADER_MODE_FIRMWARE:
            return

        self.industrial_ptc.set_wire_mode(BrickletIndustrialPTC.WIRE_MODE_2)
        self.cbe_temperature = CallbackEmulator(self.industrial_ptc.get_temperature,
                                                self.cb_temperature)
        self.cbe_temperature.set_period(100)

        self.show_device_information(device_information)

    def cb_temperature(self, temperature):
        if (1500 < temperature < 3500):
            set_value = self.mw.set_value_okay
        else:
            set_value = self.mw.set_value_error

        set_value('{0:.2f} °C'.format(temperature/100.0).replace('.', ','))
