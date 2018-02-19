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

from PyQt4 import Qt, QtGui, QtCore

from ..tinkerforge.bricklet_nfc import BrickletNFC
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde NFC Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Warte bis "Warte auf Tag" als Wert angezeigt wird
5. Tag auf Bricklet legen, ID und Typ muss angezeigt werden
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_state = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_state != None:
            self.cbe_state.set_period(0)

    def get_device_identifier(self):
        return BrickletNFC.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('nfc'))

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
            self.mw.set_value_normal("Initialisierung")
        
        elif state == self.nfc.READER_STATE_IDLE:
            self.mw.set_value_normal("Warte auf Tag")
            self.nfc.reader_request_tag_id()
            
        elif state == self.nfc.READER_STATE_REQUEST_TAG_ID:
            self.mw.set_value_normal("Warte auf Tag")
    
        elif state == self.nfc.READER_STATE_REQUEST_TAG_ID_READY:
            ret = self.nfc.reader_get_tag_id()
            
            s = 'Tag gefunden mit Typ ' + str(ret.tag_type) + ', ID [' + ' '.join(map(str, map(hex, ret.tag_id))) + "]"
            
            self.nfc.reader_request_tag_id()
            self.mw.set_value_okay(s)