# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_io16.py: IO-16 plugin

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

import math
import time
import threading

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde IO-16 Bricklet mit Port C
2. Verbinde Testadapter mit IO-16 Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Überprüfe LEDs:
     * Die LEDs blinken gleichzeitig an Port A und B
6. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

        self.running = False
        self.io16 = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        self.running = True
        self.blink_thread = threading.Thread(target=self.blick_loop)
        self.blink_thread.daemon = True
        self.blink_thread.start()

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        self.running = False

    def get_device_identifier(self):
        return BrickletIO16.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIO16.DEVICE_URL_PART))

    def blick_loop(self):
        while self.running:
            io16 = self.io16

            try:
                io16.set_port_configuration('a', 0xFF, 'o', True)
                io16.set_port_configuration('b', 0xFF, 'o', True)

                time.sleep(0.5)

                if not self.running:
                    break

                io16.set_port_configuration('a', 0xFF, 'o', False)
                io16.set_port_configuration('b', 0xFF, 'o', False)

                time.sleep(0.5)
            except Exception as e:
                print(e) # FIXME: for unknown reasons blinking doesn't work without this print
                time.sleep(0.5)

    def new_enum(self, device_information):
        self.show_device_information(device_information)

        self.io16 = BrickletIO16(device_information.uid, self.get_ipcon())
