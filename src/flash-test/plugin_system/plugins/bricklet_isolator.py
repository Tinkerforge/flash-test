# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_isolator.py: Isolator plugin

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

from ..tinkerforge.bricklet_isolator import BrickletIsolator
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Isolator Bricklet mit Port C
2. Verbinde Thermal Imaging Bricklet mit Isolator Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Öffne Thermal Imaging Bricklet im Brick Viewer und überprüfe Bild
6. Überprüfe Statistiken (Werte sollten steigen)
7. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_statistics = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_statistics:
            self.cbe_statistics.set_period(0)

    def get_device_identifier(self):
        return BrickletIsolator.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIsolator.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_statistics != None:
            self.cbe_statistics.set_period(0)

        self.isolator = BrickletIsolator(device_information.uid, self.get_ipcon())
        if self.isolator.get_bootloader_mode() != BrickletIsolator.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_statistics = CallbackEmulator(self.aout.get_statistics, self.cb_statistics)
        self.cbe_statistics.set_period(250)

        self.show_device_information(device_information)

    def cb_statistics(self, statistics):
        self.mw.set_value_normal("""Connected Bricklet UID: {3}
Connected Bricklet Device Identifier: {2}
Messages from Bricklet: {1}
Messages from Brick: {0}""".format(*statistics))
