# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_rgb_led_matrix.py: RGB LED Matrix plugin

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

from ..tinkerforge.bricklet_rgb_led_matrix import BrickletRGBLEDMatrix
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Stromversorgung (5V) mit RGB LED Matrix
2. Verbinde RGB LED Matrix mit Port C
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Überprüfe:
     * Gemessener Spannungswert sollte um die ~5V liegen
     * Farbe aller LEDs wechselt zwischen rot, grün, blau, weiß, aus
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_voltage = None
        self.color = 0

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        super().stop()
        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

    def get_device_identifier(self):
        return BrickletRGBLEDMatrix.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletRGBLEDMatrix.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)

        self.matrix = BrickletRGBLEDMatrix(device_information.uid, self.get_ipcon())
        if self.matrix.get_bootloader_mode() != BrickletRGBLEDMatrix.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_voltage = CallbackEmulator(self.matrix.get_supply_voltage,
                                            self.cb_voltage)
        self.cbe_voltage.set_period(500)

        self.show_device_information(device_information)

    def cb_voltage(self, voltage):
        if voltage > 4500 and voltage < 5500:
            self.mw.set_value_okay(str(voltage / 1000.0) + ' V')
        else:
            self.mw.set_value_error(str(voltage / 1000.0) + ' V')

        if self.color == 0:
            self.matrix.set_red([255]*64)
            self.matrix.set_green([0]*64)
            self.matrix.set_blue([0]*64)

        if self.color == 1:
            self.matrix.set_red([0]*64)
            self.matrix.set_green([255]*64)
            self.matrix.set_blue([0]*64)

        if self.color == 2:
            self.matrix.set_red([0]*64)
            self.matrix.set_green([0]*64)
            self.matrix.set_blue([255]*64)

        if self.color == 3:
            self.matrix.set_red([255]*64)
            self.matrix.set_green([255]*64)
            self.matrix.set_blue([255]*64)

        if self.color == 4:
            self.matrix.set_red([0]*64)
            self.matrix.set_green([0]*64)
            self.matrix.set_blue([0]*64)

        self.matrix.draw_frame()

        self.color = (self.color + 1) % 5
