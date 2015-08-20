# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_moisture.py: Moisture plugin

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

from ..tinkerforge.bricklet_moisture import BrickletMoisture
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Moisture Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
4. Überprüfe Wert:
     * Wert sollte sinken wenn man das Bricklet anfasst
5. Überprüfe ob Bricklet durch Gehäuseschlitz passt, eventuell nachpfeilen
6. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_moisture = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_moisture:
            self.cbe_moisture.set_period(0)

    def get_device_identifier(self):
        return BrickletMoisture.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.write_new_uid_to_bricklet()
        self.write_plugin_to_bricklet(get_bricklet_firmware_filename('moisture'))
        self.master_reset()
        
    def new_enum(self, device_information):
        self.m = BrickletMoisture(device_information.uid, self.get_ipcon())
        self.cbe_moisture = CallbackEmulator(self.m.get_moisture_value,
                                             self.cb_moisture)
        self.cbe_moisture.set_period(100)

        self.mw.set_tool_status_okay("Plugin gefunden")
            
    def cb_moisture(self, moisture):
        self.mw.set_value_normal('Feuchtewert: ' + str(moisture))
