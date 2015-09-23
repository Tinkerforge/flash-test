# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_io16.py: IO16 plugin

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

from ..tinkerforge.bricklet_io16 import BrickletIO16
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math
import time

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde IO16 Bricklet mit Port C
2. Verbinde Testadapter mit IO16 Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. Überprüfe LEDs:
     * Die LEDs blinken abwechselnd 5x zwischen Port A und B
6. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

    def start(self, device_information):
        BrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def get_device_identifier(self):
        return BrickletIO16.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('io16'))
        
    def new_enum(self, device_information):
        self.show_device_information(device_information)

        self.io16 = BrickletIO16(device_information.uid, self.get_ipcon())
            
        for i in range(5):
            time.sleep(0.2)
            self.io16.set_port_configuration('a', 0xFF, 'o', True)
            self.io16.set_port_configuration('b', 0xFF, 'o', False)
            time.sleep(0.2)
            self.io16.set_port_configuration('a', 0xFF, 'o', False)
            self.io16.set_port_configuration('b', 0xFF, 'o', True)
