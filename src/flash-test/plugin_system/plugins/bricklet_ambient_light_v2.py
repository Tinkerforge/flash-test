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

from PyQt4 import Qt, QtGui, QtCore

from ..tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from ..plugin_base import PluginBase

from ..callback_emulator import CallbackEmulator

class Plugin(PluginBase):
    TODO_TEXT = u"""\
1. Verbinde Ambient Light 2.0 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
4. Überprüfe Wert:
 * Wert sollte größer sein wenn Helligkeit steigt
 * Wert sollte zwischen ~100 und ~10000 liegen innen
5. Das Bricklet ist fertig. In kleine ESD-Tüte stecken, zuschweißen, aufkleber aufkleben.
6. Gehe zu 1
"""

    def __init__(self, *args):
        PluginBase.__init__(self, *args)
        self.cbe_illuminance = None

    def start(self, device_information):
        PluginBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_illuminance:
            self.cbe_illuminance.set_period(0)

    def get_device_identifier(self):
        return BrickletAmbientLightV2.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.write_new_uid_to_bricklet()
        self.write_plugin_to_bricklet('/home/olaf/ee/flash-test/firmwares/bricklets/ambient_light_v2/bricklet_ambient_light_v2_firmware_latest.bin')
        self.master_reset()
        
    def new_enum(self, device_information):
        if device_information:
            self.al = BrickletAmbientLightV2(device_information.uid, self.get_ipcon())
            self.al.set_configuration(BrickletAmbientLightV2.ILLUMINANCE_RANGE_8000LUX, BrickletAmbientLightV2.INTEGRATION_TIME_50MS)
            self.cbe_illuminance = CallbackEmulator(self.al.get_illuminance,
                                                    self.cb_illuminance)
            self.cbe_illuminance.set_period(100)
            
            self.mw.label_tool_status.setText("Plugin gefunden")
            
    def cb_illuminance(self, illuminance):
        self.mw.label_value.setText(str(illuminance//100) + ' Lux')