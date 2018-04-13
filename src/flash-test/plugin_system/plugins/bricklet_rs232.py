# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_rs232.py: RS232 plugin

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

from ..tinkerforge.bricklet_rs232 import BrickletRS232
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde RS232 Bricklet mit Port C
2. Setze Jumper zwischen TX und RX1
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Warte bis Wert sich auf "Test OK!" ändert
6. Setze Jumper um zwischen RX1 und RX2
7. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    qtcb_read = QtCore.pyqtSignal(object, int)

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

        self.message = b''

        self.qtcb_read.connect(self.cb_read)

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletRS232.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.mw.set_value_action("Warte auf Reset")
        QtGui.QApplication.processEvents()
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletRS232.DEVICE_URL_PART))

    def new_enum(self, device_information):
        self.rs232 = BrickletRS232(device_information.uid, self.get_ipcon())
        self.rs232.register_callback(self.rs232.CALLBACK_READ_CALLBACK, self.qtcb_read.emit)
        self.rs232.enable_read_callback()

        self.show_device_information(device_information)

        self.message = b''
        message = b'012345678\xee'*6
        self.rs232.write(message, len(message))

        self.mw.set_value_action("Warte auf Antwort")

    def cb_read(self, message, length):
        self.message += bytes([ord(x) for x in message[:length]])

        self.mw.set_value_action("Warte auf Antwort: {0} Bytes fehlen noch".format(60 - len(self.message)))

        if self.message == b'012345678\xee'*6:
            self.message = b''
            self.mw.set_value_okay("Test OK!")
