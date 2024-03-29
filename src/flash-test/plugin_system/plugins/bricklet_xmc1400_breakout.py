# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

bricklet_xmc1400_breakout.py: XMC1400 Breakout plugin

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

from ..tinkerforge.bricklet_xmc1400_breakout import BrickletXMC1400Breakout
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde XMC1400 Breakout Bricklet mit Port D des Master Bricks 3.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Prüfe ob Counter hochzählt
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_counter = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_counter != None:
            self.cbe_counter.set_period(0)

    def get_device_identifier(self):
        return BrickletXMC1400Breakout.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletXMC1400Breakout.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_counter != None:
            self.cbe_counter.set_period(0)

        self.xmc = BrickletXMC1400Breakout(device_information.uid, self.get_ipcon())
        self.cbe_counter = CallbackEmulator(self.xmc.get_count, self.cb_counter)
        self.cbe_counter.set_period(100)

        self.show_device_information(device_information)

    def cb_counter(self, counter):
        self.mw.set_value_okay(str(counter))
