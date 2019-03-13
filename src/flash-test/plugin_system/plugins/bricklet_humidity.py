# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

bricklet_humidity.py: Humidity plugin

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

from ..tinkerforge.bricklet_humidity import BrickletHumidity
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Humidity Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Wert sollte im Bereich von 30-60 %RH liegen
     * Wert sollte steigen wenn man das Bricklet anfasst
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_humidity = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_humidity != None:
            self.cbe_humidity.set_period(0)

    def get_device_identifier(self):
        return BrickletHumidity.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletHumidity.DEVICE_URL_PART))

    def new_enum(self, device_information):
        if self.cbe_humidity != None:
            self.cbe_humidity.set_period(0)

        self.h = BrickletHumidity(device_information.uid, self.get_ipcon())
        self.cbe_humidity = CallbackEmulator(self.h.get_humidity,
                                             self.cb_humidity)
        self.cbe_humidity.set_period(100)

        self.show_device_information(device_information)

    def cb_humidity(self, humidity):
        self.mw.set_value_normal(str(humidity / 10.0) + ' %RH')
