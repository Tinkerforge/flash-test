# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_analog_out_v3.py: Analog Out 3.0 plugin

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

from ..tinkerforge.bricklet_analog_out_v3 import BrickletAnalogOutV3
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
2. Verbinde Analog Out 3.0 Bricklet mit Port C
2. Verbinde Testadapter mit Analog Out 3.0 Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Überprüfe Eingangsspannung und Ausgangsspannung an VOUT und GND mit Multimeter:
     * Ausgangsspannung sollte zwischen 2.9 und 3.1 V liegen
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_input_voltage = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_input_voltage:
            self.cbe_input_voltage.set_period(0)

    def get_device_identifier(self):
        return BrickletAnalogOutV3.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletAnalogOutV3.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_input_voltage != None:
            self.cbe_input_voltage.set_period(0)

        self.aout = BrickletAnalogOutV3(device_information.uid, self.get_ipcon())
        if self.aout.get_bootloader_mode() != BrickletAnalogOutV3.BOOTLOADER_MODE_FIRMWARE:
            return

        self.aout.set_output_voltage(3000)
        self.cbe_input_voltage = CallbackEmulator(self.aout.get_input_voltage, self.cb_input_voltage)
        self.cbe_input_voltage.set_period(100)

        self.show_device_information(device_information)
        self.mw.set_value_normal("3V angelegt")

    def cb_input_voltage(self, voltage):
        # FIXME: only show input colored
        value = 'Eingang: ' + str(round(voltage/1000.0, 2)) + ' V, Ausgang: 3.00 V'

        if voltage < 4500 or voltage > 5500:
            self.mw.set_value_error(value)
        else:
            self.mw.set_value_okay(value)
