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

from PyQt4 import Qt, QtGui, QtCore

from ..tinkerforge.bricklet_uv_light_v2 import BrickletUVLightV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde UV Light Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Wert sollten größer werden wenn Bricklet direkt an eine Lampe gehalten wird
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_uv_light = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_uv_light != None:
            self.cbe_uv_light.set_period(0)

    def get_device_identifier(self):
        return BrickletUVLightV2.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletUVLightV2.DEVICE_URL_PART))
        
    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_uv_light != None:
            self.cbe_uv_light.set_period(0)

        self.uv = BrickletUVLightV2(device_information.uid, self.get_ipcon())
        if self.uv.get_bootloader_mode() != BrickletUVLightV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_uv_light = CallbackEmulator(self.uv.get_uva, self.cb_uva)
        self.cbe_uv_light.set_period(250)
        self.show_device_information(device_information)
            
    def cb_uva(self, uva):
        uvb = self.uv.get_uvb()
        uvi = self.uv.get_uvi()
        self.mw.set_value_normal('UVA: {0} mW/m², UVB: {1} mW/m², UVI: {2} mW/m²'.format(uva, uvb, uvi))
