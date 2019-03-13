# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_e_paper_296x128.py: E-Paper 296x128 plugin

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

from ..tinkerforge.bricklet_e_paper_296x128 import BrickletEPaper296x128
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator
from ..pixel_data import e_paper_pixels_bw, e_paper_pixels_red

STATE_VERTICAL = 0
STATE_HORIZONTAL = 1
STATE_ALL_ON = 2

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde E-Paper 296x128 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Tinkerforge Logo wird auf Bildschirm dargestellt
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletEPaper296x128.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletEPaper296x128.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.epaper = BrickletEPaper296x128(device_information.uid, self.get_ipcon())
        if self.epaper.get_bootloader_mode() != BrickletEPaper296x128.BOOTLOADER_MODE_FIRMWARE:
            return

        self.epaper.set_update_mode(0)
        self.epaper.write_black_white(0, 0, 295, 127, e_paper_pixels_bw)
        self.epaper.write_color(0, 0, 295, 127, e_paper_pixels_red)
        self.epaper.draw()
