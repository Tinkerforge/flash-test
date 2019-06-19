# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_ambient_light_v2.py: Ambient Light 2.0 plugin

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

from ..tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Ambient Light 2.0 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Wert sollte größer sein wenn Helligkeit steigt
     * Wert sollte zwischen ~100 und ~10000 liegen
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_illuminance = None

    def start(self):
        BrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_illuminance != None:
            self.cbe_illuminance.set_period(0)

    def get_device_identifier(self):
        return BrickletAmbientLightV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletAmbientLightV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        if self.cbe_illuminance != None:
            self.cbe_illuminance.set_period(0)

        self.al = BrickletAmbientLightV2(device_information.uid, self.get_ipcon())
        self.al.set_configuration(BrickletAmbientLightV2.ILLUMINANCE_RANGE_8000LUX, BrickletAmbientLightV2.INTEGRATION_TIME_50MS)
        self.cbe_illuminance = CallbackEmulator(self.al.get_illuminance,
                                                self.cb_illuminance)
        self.cbe_illuminance.set_period(100)

        self.show_device_information(device_information)

    def cb_illuminance(self, illuminance):
        self.mw.set_value_normal(str(illuminance//100) + ' Lux')
