# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_uv_light_v2.py: UV Light 2.0 plugin

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

from ..tinkerforge.bricklet_uv_light_v2 import BrickletUVLightV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde UV Light Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * UVI Wert sollte im Büro 0 sein
     * UVA/B Werte sollten im Büro zwischen 20 und 200 mW/m² liegen und sinken wenn der Sensor beschattet wird
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_uva = None
        self.cbe_uvb = None
        self.cbe_uvi = None
        self.last_uva = 0
        self.last_uvb = 0
        self.last_uvi = 0

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_uva != None:
            self.cbe_uva.set_period(0)

    def get_device_identifier(self):
        return BrickletUVLightV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletUVLightV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_uva != None:
            self.cbe_uva.set_period(0)

        self.uv = BrickletUVLightV2(device_information.uid, self.get_ipcon())
        if self.uv.get_bootloader_mode() != BrickletUVLightV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.last_uva = 0
        self.last_uvb = 0
        self.last_uvi = 0

        self.uv.set_configuration(0) # 50ms
        self.cbe_uva = CallbackEmulator(self.uv.get_uva, self.cb_uva)
        self.cbe_uva.set_period(50)
        self.cbe_uvb = CallbackEmulator(self.uv.get_uvb, self.cb_uvb)
        self.cbe_uvb.set_period(50)
        self.cbe_uvi = CallbackEmulator(self.uv.get_uvi, self.cb_uvi)
        self.cbe_uvi.set_period(50)
        self.show_device_information(device_information)

    def update_values(self, uva, uvb, uvi):
        self.mw.set_value_normal('UVA: {0} mW/m², UVB: {1} mW/m², UVI: {2}'.format(uva / 10.0, uvb / 10.0, uvi / 10.0))

    def cb_uva(self, uva):
        self.last_uva = uva
        self.update_values(uva, self.last_uvb, self.last_uvi)

    def cb_uvb(self, uvb):
        self.last_uvb = uvb
        self.update_values(self.last_uva, uvb, self.last_uvi)

    def cb_uvi(self, uvi):
        self.last_uvi = uvi
        self.update_values(self.last_uva, self.last_uvb, uvi)
