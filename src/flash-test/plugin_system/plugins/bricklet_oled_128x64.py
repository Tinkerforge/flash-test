# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Olaf Lüke <olaf@tinkerforge.com>

bricklet_oled_128x64.py: OLED 128x64 plugin

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

from ..tinkerforge.bricklet_oled_128x64 import BrickletOLED128x64
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
2. Verbinde OLED 128x64 Bricklet mit Port C
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. Streifen wandert auf Display Vertikal und Horizontal
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.vertical = True
        self.num = 0
        self.cbe_state = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletOLED128x64.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('oled_128x64'))
        if self.cbe_state != None:
            self.cbe_state.set_period(0)

    def new_enum(self, device_information):
        self.oled = BrickletOLED128x64(device_information.uid, self.get_ipcon())
        self.cbe_state = CallbackEmulator(self.oled.get_api_version, self.cb, ignore_last_data=True)
        self.cbe_state.set_period(25)

        self.show_device_information(device_information)

    def cb(self, _):
        self.oled.new_window(0, 127, 0, 7)
        if self.vertical:
            for i in range(8):
                line = [0]*64
                if i == self.num//8:
                    line = [1 << (self.num % 8)]*64
                self.oled.write(line)
                
                line = [0]*64
                if i == self.num//8:
                    line = [1 << (self.num % 8)]*64
                self.oled.write(line)
        else:
            for i in range(8):
                line = [0]*64
                if self.num < 64:
                    line[self.num] = 0xFF 
                self.oled.write(line)
                
                line = [0]*64
                if self.num >= 64:
                    line[self.num-64] = 0xFF 
                self.oled.write(line)

        self.num += 1
        
        if self.vertical:
            if self.num >= 64:
                self.num = 0
                self.vertical = False
        else:
            if self.num >= 128:
                self.num = 0
                self.vertical = True
