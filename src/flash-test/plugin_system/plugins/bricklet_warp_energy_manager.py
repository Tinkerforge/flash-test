# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2023 Olaf Lüke <olaf@tinkerforge.com>

bricklet_warp_energy_manager.py: WARP Energy Manager plugin

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

from ..tinkerforge.bricklet_warp_energy_manager import BrickletWARPEnergyManager
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Verbinde WARP Energy Manager Bricklet mit Port D des Master Bricks 3.0
1. Verbinde WARP Energy Manager Bricklet Testadapter mit Port C
2. Drücke Bricklet in Tester herunter bis es kontaktiert
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Prüfe ob LED zwischen rot, grün, blau und weiß hin und her wechselt.
6. Das Bricklet ist fertig
7. Gehe zu 1
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
        return BrickletWARPEnergyManager.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletWARPEnergyManager.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_counter != None:
            self.cbe_counter.set_period(0)

        self.wem = BrickletWARPEnergyManager(device_information.uid, self.get_ipcon())
        if self.wem.get_bootloader_mode() != BrickletWARPEnergyManager.BOOTLOADER_MODE_FIRMWARE:
            return
        
        self.cbe_rgb_value = CallbackEmulator(self.wem.get_rgb_value, self.cb_rgb_value)
        self.cbe_rgb_value.set_period(500)

        self.show_device_information(device_information)

    def cb_rgb_value(self, value):
        r = value.r
        g = value.g
        b = value.b

        r_new = 0
        g_new = 0
        b_new = 0

        if r == 255 and g == 255 and b == 255:
            r_new = 255
            g_new = 0
            b_new = 0
        elif r == 255:
            r_new = 0
            g_new = 255
            b_new = 0
        elif g == 255:
            r_new = 0
            g_new = 0
            b_new = 255
        else:
            r_new = 255
            g_new = 255
            b_new = 255

        self.wem.set_rgb_value(r_new, g_new, b_new)