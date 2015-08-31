# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_analog_out_v2.py: Analog Out 2.0 plugin

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

from ..tinkerforge.bricklet_analog_out_v2 import BrickletAnalogOutV2
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Analog Out 2.0 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
4. Überprüfe Wert mit Multimeter:
     * Spannung sollte mit eingespeister Spannung übereinstimmen
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_voltage = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_voltage:
            self.cbe_voltage.set_period(0)

    def get_device_identifier(self):
        return BrickletAnalogOutV2.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.write_new_uid_to_bricklet()
        self.write_plugin_to_bricklet(get_bricklet_firmware_filename('analog_out_v2'))
        self.master_reset()
        
    def new_enum(self, device_information):
        self.aout = BrickletAnalogOutV2(device_information.uid, self.get_ipcon())
        self.aout.set_output_voltage(3000)

        self.mw.set_tool_status_okay("Plugin gefunden")
        self.mw.set_value_okay("3.0V angelegt")

