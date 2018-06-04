# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_load_cell_v2.py: Load Cell 2.0 plugin

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

from ..tinkerforge.bricklet_load_cell_v2 import BrickletLoadCellV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Load Cell 2.0 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert:
     * Stecke Bricklet in Testaufbau, überprüfe ob Wert steigt wenn auf Wägezelle gedrückt wird
     * LED muss dabei durchgängig blinken
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_weight = None
        self.led_is_on = False

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_weight != None:
            self.cbe_weight.set_period(0)

    def get_device_identifier(self):
        return BrickletLoadCellV2.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletLoadCellV2.DEVICE_URL_PART))
        
    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_weight != None:
            self.cbe_weight.set_period(0)

        self.load_cell_v2 = BrickletLoadCellV2(device_information.uid, self.get_ipcon())
        if self.load_cell_v2.get_bootloader_mode() != BrickletLoadCellV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_weight = CallbackEmulator(self.load_cell_v2.get_weight,
                                           self.cb_weight)
        self.cbe_weight.set_period(100)

        self.show_device_information(device_information)
            
    def cb_weight(self, weight):
        if self.load_cell_v2.get_info_led_config() == BrickletLoadCellV2.INFO_LED_CONFIG_ON:
            self.load_cell_v2.set_info_led_config(BrickletLoadCellV2.INFO_LED_CONFIG_OFF)
        else:
            self.load_cell_v2.set_info_led_config(BrickletLoadCellV2.INFO_LED_CONFIG_ON)
        
        self.mw.set_value_normal('Gewichtswert: ' + str(weight))
