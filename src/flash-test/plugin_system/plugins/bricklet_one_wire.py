# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_one_wire.py: One Wire plugin

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

from ..tinkerforge.bricklet_one_wire import BrickletOneWire
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde One Wire Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Stecke Jumper of 3.3V-Stellung
5. Verbinde MAX31820 mit One Wire Bricklet
6. Überprüfe Wert:
     * Wert sollte beim Berühren des Sensors steigt
     * Wert sollte zwischen ~20 und ~30 liegen
7. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe != None:
            self.cbe.set_period(0)

    def get_device_identifier(self):
        return BrickletOneWire.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletOneWire.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe != None:
            self.cbe.set_period(0)

        self.ow = BrickletOneWire(device_information.uid, self.get_ipcon())
        if self.ow.get_bootloader_mode() != BrickletOneWire.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe = CallbackEmulator(self.ow.get_communication_led_config, self.cb, ignore_last_data=True)

        self.ow.write_command(0, 0x4E)     # WRITE SCRATCHPAD
        self.ow.write(0x00)                # ALARM H (unused)
        self.ow.write(0x00)                # ALARM L (unused)
        self.ow.write(0x7F)                # COFIGURATION: 12 bit mode
        self.ow.write_command(0, 0x44)     # CONVERT T (start temperature conversion)
        self.cbe.set_period(250)

        self.show_device_information(device_information)

    def cb(self, _):
        self.ow.write_command(0, 0xBE) # READ SCRATCHPAD

        t_low = self.ow.read().data    # Read LSB
        t_high = self.ow.read().data   # Read MSB

        temperature = (t_low | (t_high << 8))/16.0
        if (15.00 < temperature < 35.00):
            set_value = self.mw.set_value_okay
        else:
            set_value = self.mw.set_value_error

        set_value('Temperatur: {0} °C'.format(temperature))

        self.ow.write_command(0, 0x44) # CONVERT T (start temperature conversion)