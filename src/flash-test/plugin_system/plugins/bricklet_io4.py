# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Matthias Bolte <matthias@tinkerforge.com>

bricklet_io4.py: IO-4 plugin

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

from ..tinkerforge.bricklet_io4 import BrickletIO4
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

import math
import time

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde IO-4 Bricklet mit Port C
2. Verbinde Testadapter mit IO-4 Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Überprüfe LEDs:
     * Die LEDs blinken 5x
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
        return BrickletIO4.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIO4.DEVICE_URL_PART))
        
    def new_enum(self, device_information):
        self.show_device_information(device_information)

        self.io4 = BrickletIO4(device_information.uid, self.get_ipcon())
            
        for i in range(5):
            time.sleep(0.2)
            self.io4.set_configuration(0xFF, 'o', True)
            time.sleep(0.2)
            self.io4.set_configuration(0xFF, 'o', False)
