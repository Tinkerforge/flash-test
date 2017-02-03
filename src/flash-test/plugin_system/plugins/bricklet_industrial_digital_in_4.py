# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_digital_in_4.py: Industrial Digital In 4 plugin

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

from ..tinkerforge.bricklet_industrial_digital_in_4 import BrickletIndustrialDigitalIn4
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Digital In 4 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Drücke Knöpfe und überpüfe Werte.
5. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_value = None
        
        self.last_values = None
        self.changes = [0, 0, 0, 0]

    def start(self, device_information):
        BrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletIndustrialDigitalIn4.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('industrial_digital_in_4'))
        
    def new_enum(self, device_information):
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.changes = [0, 0, 0, 0]
        self.last_values = None
        self.industrial_digital_in_4 = BrickletIndustrialDigitalIn4(device_information.uid, self.get_ipcon())
        self.cbe_value = CallbackEmulator(self.industrial_digital_in_4.get_value, self.cb_value)
        self.cbe_value.set_period(100)

        self.show_device_information(device_information)
            
    def cb_value(self, value):
        values = [value & 1, (value >> 1) & 1, (value >> 2) & 1, (value >> 3) & 1]
        if self.last_values == None:
            self.last_values = values
        else:
            for i in range(4):
                if self.last_values[i] != values[i]:
                    self.changes[i] += 1
            self.last_values = values

        show = []
        for i in range(4):
            if self.changes[i] > 1:
                show.append('\u2611')
            else:
                show.append(values[i])
        
        set_value = self.mw.set_value_action
        if show[0] == '\u2611' and show[1] == '\u2611' and show[2] == '\u2611' and show[3] == '\u2611':
            set_value =  self.mw.set_value_okay
        
        set_value("Werte: {0} {1} {2} {3} (0 = Masse, 1 = 24V, \u2611 = OK)".format(show[0], show[1], show[2], show[3]))
