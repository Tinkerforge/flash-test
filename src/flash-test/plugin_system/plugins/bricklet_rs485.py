# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_rs485.py: RS485 plugin

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

from PyQt5 import Qt, QtGui, QtCore

from ..tinkerforge.bricklet_rs485 import BrickletRS485
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import traceback

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. DIP Schalter auf 1=ON, 2=OFF, 3=OFF, 4=OFF stellen
2. Verbinde TX+/- mit RX+/-
3. Verbinde RS485 Bricklet mit Flash Adapter XMC
4. Drücke "Flashen"
5. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
6. Überprüfe Wert: "Test OK!"
7. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)

    def start(self):
        CoMCUBrickletBase.start(self)

    def get_device_identifier(self):
        return BrickletRS485.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletRS485.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.rs485 = BrickletRS485(device_information.uid, self.get_ipcon())
        if self.rs485.get_bootloader_mode() != BrickletRS485.BOOTLOADER_MODE_FIRMWARE:
            return

        self.rs485.set_rs485_configuration(115200, BrickletRS485.PARITY_NONE, BrickletRS485.STOPBITS_1, BrickletRS485.WORDLENGTH_8, BrickletRS485.DUPLEX_FULL)
        self.rs485.set_mode(BrickletRS485.MODE_RS485)

        BYTES_TO_SEND = 1280

        # Bring data in same format as output will be
        data_in = [(chr(x % 256)) for x in range(BYTES_TO_SEND)]

        try:
            self.rs485.write(data_in)
            data_out = []
            start = time.time()
            current = time.time()
            while current - start < 1 and len(data_out) < BYTES_TO_SEND:
                data_out.extend(self.rs485.read(BYTES_TO_SEND))
                current = time.time()
                self.mw.set_value_action("Warte auf Antwort: {0} Bytes fehlen noch".format(BYTES_TO_SEND - len(data_out)))

            if current - start >= 1 or len(data_out) < BYTES_TO_SEND:
                self.mw.set_value_error("Timeout!")
            elif data_in != data_out:
                self.mw.set_value_error("Fehler während Übertragung!")
            else:
                self.mw.set_value_okay("Test OK!")
        except:
            self.mw.set_value_error("Fehler: " + traceback.format_exc())

