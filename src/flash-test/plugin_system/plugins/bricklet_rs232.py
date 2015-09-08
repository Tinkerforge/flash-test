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
from ..callback_emulator import CallbackEmulator

def string_to_char_list(message):
    chars = [bytes([x]) for x in list(message)]
    chars.extend([b'\0']*(60 - len(message)))
    return chars, len(message)

def char_list_to_string(message, length):
    chars = []

    for c in message[:length]:
        if type(c) == str:
            c = c.encode('ascii')

        chars.append(c)

    return b''.join(chars)

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde RS232 Bricklet mit Port C
2. Setze Jumper zwischen TX und RX1
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. Warte bis Wert sich auf "Test OK!" ändert
6. Setze Jumper um zwischen RX1 und RX2
7. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
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
        self.write_new_uid_to_bricklet()
        self.write_plugin_to_bricklet(get_bricklet_firmware_filename('rs232'))
        self.master_reset()

    def new_enum(self, device_information):
        self.rs232 = BrickletRS232(device_information.uid, self.get_ipcon())
        self.rs232.register_callback(self.rs232.CALLBACK_READ_CALLBACK, self.qtcb_read.emit)
        self.rs232.enable_read_callback()

        self.mw.set_tool_status_okay("Plugin gefunden")

        self.message = b''
        self.rs232.write(*string_to_char_list(b'012345678\xee'*6))

        self.mw.set_value_action("Warte auf Antwort")

    def cb_read(self, message, length):
        s = char_list_to_string(message, length)
        self.message += s

        self.mw.set_value_action("Warte auf Antwort: {0} Bytes fehlen noch".format(60 - len(self.message)))

        if self.message == b'012345678\xee'*6:
            self.message = b''
            self.mw.set_value_okay("Test OK!")
