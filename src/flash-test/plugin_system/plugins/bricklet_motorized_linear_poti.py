# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_motorized_linear_poti.py: Motorized Linear Poti plugin

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

from ..tinkerforge.bricklet_motorized_linear_poti import BrickletMotorizedLinearPoti
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Motorized Linear Poti mit Port D des Master Bricks 3.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Überprüfe:
     * Kalibrierung wird ausgeführt (Poti fährt von in beide Anschläge)
     * Position ändert sich wenn Slider verschoben wird. Fahre 0 oben und 100 unten an. Text wird grün.
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_position = None
        self.seen0 = False
        self.seen100 = False
        self.counter = 0

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_position != None:
            self.cbe_position.set_period(0)

    def get_device_identifier(self):
        return BrickletMotorizedLinearPoti.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletMotorizedLinearPoti.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_position != None:
            self.cbe_position.set_period(0)

        self.seen0 = False
        self.seen100 = False

        self.mlp = BrickletMotorizedLinearPoti(device_information.uid, self.get_ipcon())
        if self.mlp.get_bootloader_mode() != BrickletMotorizedLinearPoti.BOOTLOADER_MODE_FIRMWARE:
            return

        self.mlp.calibrate()
        self.cbe_position = CallbackEmulator(self.mlp.get_position,
                                             self.cb_position,
                                             ignore_last_data=True)
        self.cbe_position.set_period(50)

        self.show_device_information(device_information)
        self.mw.set_value_normal('Kalibriere...')

    def cb_position(self, position):
        # Throw away first data during calibration
        self.counter += 1
        if self.counter < 10:
            return

        if position == 0:
            self.seen0 = True
        elif position == 100:
            self.seen100 = True

        set_value = self.mw.set_value_normal
        if self.seen0 and self.seen100:
            set_value = self.mw.set_value_okay

        set_value('Position: {0}'.format(position))
