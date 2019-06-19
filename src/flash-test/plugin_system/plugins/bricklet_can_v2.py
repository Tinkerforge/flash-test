# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Matthias Bolte <matthias@tinkerforge.com>

bricklet_can_v2.py: CAN 2.0 plugin

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

from ..tinkerforge.bricklet_can_v2 import BrickletCANV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde CAN Bricklet 2.0 mit Port C
2. Schalte Terminierung am CAN Bricklet 2.0 ein
3. Verbinde CAN Bricklet 2.0 mit Testadapter
4. Drücke "Flashen"
5. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
6. Warte bis Wert sich auf "Test OK!" ändert
7. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    qtcb_frame_read = QtCore.pyqtSignal(int, int, object)

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)

        self.qtcb_frame_read.connect(self.cb_frame_read)

    def start(self):
        CoMCUBrickletBase.start(self)

    def get_device_identifier(self):
        return BrickletCANV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletCANV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.can = BrickletCANV2(device_information.uid, self.get_ipcon())
        if self.can.get_bootloader_mode() != BrickletCANV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.can.register_callback(self.can.CALLBACK_FRAME_READ, self.qtcb_frame_read.emit)
        self.can.set_frame_read_callback_configuration(True)

        self.show_device_information(device_information)

        self.can.write_frame(self.can.FRAME_TYPE_STANDARD_DATA, 1742, [42, 23, 17])

        self.mw.set_value_action("Warte auf Antwort")

    def cb_frame_read(self, frame_type, identifier, data):
        if frame_type == self.can.FRAME_TYPE_STANDARD_DATA and \
           identifier == 1742 and \
           data == (42, 23, 17):
            self.mw.set_value_okay("Test OK!")
        else:
            self.mw.set_value_error("Test fehlgeschlagen!")
