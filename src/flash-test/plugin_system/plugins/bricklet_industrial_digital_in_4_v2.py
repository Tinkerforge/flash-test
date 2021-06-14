# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_digital_in_4_v2.py: Industrial Digital In 4 2.0 plugin

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

from ..tinkerforge.bricklet_industrial_digital_in_4_v2 import BrickletIndustrialDigitalIn4V2
from ..tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Digital In 4 Bricklet 2.0 mit Port D des Master Bricks 3.0
2. Verbinde Testadapter mit Industrial Digital In 4 Bricklet 2.0
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Testadapter schaltet automatisch durch, überpüfe Werte und Status LEDs (Reihenfolge: alle aus, 0, 1, 2, 3, alle an).
6. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_value = None

        self.relay = None
        self.relay_value = 0
        self.last_values = None
        self.changes = [0, 0, 0, 0]

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletIndustrialDigitalIn4V2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialDigitalIn4V2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.changes = [0, 0, 0, 0]
        self.relay_value = 0
        self.last_values = None
        self.industrial_digital_in_4_v2 = BrickletIndustrialDigitalIn4V2(device_information.uid, self.get_ipcon())
        if self.industrial_digital_in_4_v2.get_bootloader_mode() != BrickletIndustrialDigitalIn4V2.BOOTLOADER_MODE_FIRMWARE:
            return

        if self.relay == None:
            self.relay = BrickletIndustrialQuadRelayV2('test', self.get_ipcon())

            try:
                self.relay.get_identity()
            except:
                self.relay = None

        self.cbe_value = CallbackEmulator(self.industrial_digital_in_4_v2.get_value, self.cb_value, ignore_last_data=True)
        self.cbe_value.set_period(250)

        self.show_device_information(device_information)

    def cb_value(self, values):
        if self.relay != None:
            if self.relay_value == 0:
                self.relay.set_value((True, False, False, False))
            if self.relay_value == 1:
                self.relay.set_value((False, True, False, False))
            if self.relay_value == 2:
                self.relay.set_value((False, False, True, False))
            if self.relay_value == 3:
                self.relay.set_value((False, False, False, True))
            if self.relay_value == 4:
                self.relay.set_value((True, True, True, True))
            if self.relay_value == 5:
                self.relay.set_value((False, False, False, False))

            self.relay_value = (self.relay_value + 1) % 6

        if self.last_values == None:
            self.last_values = values
        else:
            for i in range(4):
                if self.last_values[i] != values[i]:
                    self.changes[i] += 1
            self.last_values = values

        show = []
        for i in range(4):
            if self.changes[i] > 1:
                show.append('\u2611')
            else:
                show.append(1 if values[i] else 0)

        set_value = self.mw.set_value_action
        if show[0] == '\u2611' and show[1] == '\u2611' and show[2] == '\u2611' and show[3] == '\u2611':
            set_value =  self.mw.set_value_okay

        set_value("Werte: {0} {1} {2} {3} (0 = Masse, 1 = 24V, \u2611 = OK)".format(show[0], show[1], show[2], show[3]))
