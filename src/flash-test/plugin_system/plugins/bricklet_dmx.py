# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2017 Olaf Lüke <olaf@tinkerforge.com>

bricklet_dmx.py: DMX plugin

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

from ..tinkerforge.bricklet_dmx import BrickletDMX
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde DMX Bricklet mit Port C
2. Verbinde DMX Master mit Bricklet (DMX Master ist am selben Master Brick)
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Knopf drücken uns loslassen
5. Überprüfe:
     * "Daten empfangen und überprüft" wird angezeigt
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)

    def start(self):
        CoMCUBrickletBase.start(self)

    def get_device_identifier(self):
        return BrickletDMX.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletDMX.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.dmx_master = BrickletDMX('dmxT1', self.get_ipcon())
        self.dmx_master.set_dmx_mode(0)
        self.dmx_master.write_frame(list(range(256))*2)

        self.dmx_slave = BrickletDMX(device_information.uid, self.get_ipcon())
        if self.dmx_slave.get_bootloader_mode() != BrickletDMX.BOOTLOADER_MODE_FIRMWARE:
            return

        self.dmx_slave.set_dmx_mode(1)
        self.cbe_read_frame = CallbackEmulator(self.dmx_slave.read_frame,
                                               self.cb_read_frame)
        self.cbe_read_frame.set_period(250)

        self.show_device_information(device_information)

    def cb_read_frame(self, frame):
        if frame.frame == ():
            self.mw.set_value_normal('Warte auf Daten')
        elif frame.frame == tuple(list(range(256))*2):
            self.mw.set_value_okay('Daten empfangen und überprüft')
        else:
            self.mw.set_value_error('Fehler in Daten: {0}', str(frame.frame))
