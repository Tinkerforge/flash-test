# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

bricklet_can.py: CAN plugin

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

from PyQt5 import Qt, QtWidgets, QtCore

from ..tinkerforge.bricklet_can import BrickletCAN
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde CAN Bricklet mit Port C
2. Schalte Terminierung am CAN Bricklet ein
3. Verbinde CAN Bricklet mit Testadapter
4. Drücke "Flashen"
5. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
6. Warte bis Wert sich auf "Test OK!" ändert
7. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    qtcb_frame_read = QtCore.pyqtSignal(int, int, object, int)

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

        self.qtcb_frame_read.connect(self.cb_frame_read)

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def get_device_identifier(self):
        return BrickletCAN.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.mw.set_value_action("Warte auf Reset")
        QtWidgets.QApplication.processEvents()
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletCAN.DEVICE_URL_PART))

    def new_enum(self, device_information):
        self.can = BrickletCAN(device_information.uid, self.get_ipcon())
        self.can.register_callback(self.can.CALLBACK_FRAME_READ, self.qtcb_frame_read.emit)
        self.can.enable_frame_read_callback()

        self.show_device_information(device_information)

        self.can.write_frame(self.can.FRAME_TYPE_STANDARD_DATA, 1742, [42, 23, 17, 0, 0, 0, 0, 0], 3)

        self.mw.set_value_action("Warte auf Antwort")

    def cb_frame_read(self, frame_type, identifier, data, length):
        if frame_type == self.can.FRAME_TYPE_STANDARD_DATA and \
           identifier == 1742 and \
           data[:3] == (42, 23, 17) and \
           length == 3:
            self.mw.set_value_okay("Test OK!")
        else:
            self.mw.set_value_error("Test fehlgeschlagen!")
