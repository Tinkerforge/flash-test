# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias <matthias@tinkerforge.com>

bricklet_multi_touch.py: Multi Touch plugin

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

from ..tinkerforge.bricklet_multi_touch import BrickletMultiTouch
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Multi Touch Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. Überprüfe Elektorden:
     * Berührte Elektorden müssen grün angeteigt werden
6. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_touch_state = None

    def start(self, device_information):
        BrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_touch_state:
            self.cbe_touch_state.set_period(0)

        l = self.mw.multi_touch_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

    def get_device_identifier(self):
        return BrickletMultiTouch.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('multi_touch'))
        
    def new_enum(self, device_information):
        l = self.mw.multi_touch_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)
        
        self.labels = [self.mw.label_multi_touch_0,
                       self.mw.label_multi_touch_1,
                       self.mw.label_multi_touch_2,
                       self.mw.label_multi_touch_3,
                       self.mw.label_multi_touch_4,
                       self.mw.label_multi_touch_5,
                       self.mw.label_multi_touch_6,
                       self.mw.label_multi_touch_7,
                       self.mw.label_multi_touch_8,
                       self.mw.label_multi_touch_9,
                       self.mw.label_multi_touch_10,
                       self.mw.label_multi_touch_11]

        self.mt = BrickletMultiTouch(device_information.uid, self.get_ipcon())
        self.cbe_touch_state = CallbackEmulator(self.mt.get_touch_state, self.cb_touch_state)
        self.cbe_touch_state.set_period(100)

        self.show_device_information(device_information)
            
    def cb_touch_state(self, state):
        for i in range(12):
            if state & (1 << i):
                self.labels[i].setStyleSheet("QLabel { background-color : green; }")
            else:
                self.labels[i].setStyleSheet("QLabel { background-color : black; }")
