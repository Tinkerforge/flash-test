# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_analog_in_v2.py: Analog In 2.0 plugin

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

from ..tinkerforge.bricklet_analog_in_v2 import BrickletAnalogInV2
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Analog In 2.0 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Speise 24V an VIN und GND ein
5. Überprüfe Wert:
     * Spannung sollte mit eingespeister Spannung übereinstimmen
     * Abweichungen bis 0,1V sind okay
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_voltage = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

    def get_device_identifier(self):
        return BrickletAnalogInV2.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('analog_in_v2'))
        
    def new_enum(self, device_information):
        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

        self.al = BrickletAnalogInV2(device_information.uid, self.get_ipcon())
        self.cbe_voltage = CallbackEmulator(self.al.get_voltage,
                                            self.cb_voltage)
        self.cbe_voltage.set_period(100)

        self.show_device_information(device_information)
            
    def cb_voltage(self, voltage):
        self.mw.set_value_normal(str(round(voltage/1000.0, 2)) + ' V')
