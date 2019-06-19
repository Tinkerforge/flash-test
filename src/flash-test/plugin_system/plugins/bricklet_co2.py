# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_co2.py: CO2 plugin

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

from ..tinkerforge.bricklet_co2 import BrickletCO2
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde CO2 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Wert sollte zwische 400 und 1000 liegen
5. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_co2 = None

    def start(self):
        BrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_co2 != None:
            self.cbe_co2.set_period(0)

    def get_device_identifier(self):
        return BrickletCO2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletCO2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        if self.cbe_co2 != None:
            self.cbe_co2.set_period(0)

        self.co2 = BrickletCO2(device_information.uid, self.get_ipcon())
        self.cbe_co2 = CallbackEmulator(self.co2.get_co2_concentration,
                                        self.cb_co2)
        self.cbe_co2.set_period(100)

        self.show_device_information(device_information)

    def cb_co2(self, co2):
        self.mw.set_value_normal(str(co2) + ' ppm')
