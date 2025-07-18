# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_nfc.py: NFC plugin

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

from ..tinkerforge.bricklet_nfc import BrickletNFC
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Connect NFC Bricklet with port D of the Master Brick 3.0
2. Put NFC tag on bricklet
3. Press "Flash"
4. Wait for Master Brick restart (Tool status changes to "Plugin found")
5. Wait until "Waiting for tag" is shown
6. Wait until "Tag found [...]" is shown
7. Bricklet is ready, put in standard ESD bag, weld shut, stick label on bag
8. Go to 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_state = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_state != None:
            self.cbe_state.set_period(0)

    def get_device_identifier(self):
        return BrickletNFC.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletNFC.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_state != None:
            self.cbe_state.set_period(0)

        self.nfc = BrickletNFC(device_information.uid, self.get_ipcon())
        if self.nfc.get_bootloader_mode() != BrickletNFC.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_state = CallbackEmulator(self.nfc.reader_get_state,
                                          self.cb_state)
        self.cbe_state.set_period(100)

        self.show_device_information(device_information)

    def cb_state(self, value):
        state, idle = value

        if state == self.nfc.READER_STATE_INITIALIZATION:
            self.nfc.set_mode(self.nfc.MODE_READER)
            self.mw.set_value_normal("Initialization")

        elif state == self.nfc.READER_STATE_IDLE:
            self.mw.set_value_normal("Waiting for tag")
            self.nfc.reader_request_tag_id()

        elif state == self.nfc.READER_STATE_REQUEST_TAG_ID:
            self.mw.set_value_normal("Waiting for tag")

        elif state == self.nfc.READER_STATE_REQUEST_TAG_ID_READY:
            ret = self.nfc.reader_get_tag_id()

            s = 'Tag found with type ' + str(ret.tag_type) + ', ID [' + ' '.join(map(str, map(hex, ret.tag_id))) + "]"

            self.nfc.reader_request_tag_id()
            self.mw.set_value_okay(s)

        elif state == self.nfc.READER_STATE_REQUEST_TAG_ID_ERROR:
            self.mw.set_value_normal("Waiting for tag")
            self.nfc.reader_request_tag_id()
