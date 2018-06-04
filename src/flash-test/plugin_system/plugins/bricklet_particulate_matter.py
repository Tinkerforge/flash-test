# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_particulate_matter_v2.py: Particulate Matter plugin

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

from ..tinkerforge.bricklet_particulate_matter import BrickletParticulateMatter
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
0. Entferne untere Folie von Sensor, klebe Sensor auf Bricklet
1. Verbinde Particulate Matter Bricklet mit 2.0 Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Werte: PM Konzentration zwischen 5 und 50.
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.pm_concentration = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.pm_concentration != None:
            self.pm_concentration.set_period(0)

    def get_device_identifier(self):
        return BrickletParticulateMatter.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletParticulateMatter.DEVICE_URL_PART))
        
    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.pm_concentration != None:
            self.pm_concentration.set_period(0)

        self.particulate_matter = BrickletParticulateMatter(device_information.uid, self.get_ipcon())
        if self.particulate_matter.get_bootloader_mode() != BrickletParticulateMatter.BOOTLOADER_MODE_FIRMWARE:
            return
        
        self.pm_concentration = CallbackEmulator(self.particulate_matter.get_pm_concentration,
                                                 self.cb_pm_concentration)
        self.pm_concentration.set_period(100)

        self.show_device_information(device_information)
            
    def cb_pm_concentration(self, pm):
        if (5 < pm.pm10 < 50) and (5 < pm.pm25 < 50) and (5 < pm.pm100 < 50):
            set_value = self.mw.set_value_okay
        else:
            set_value = self.mw.set_value_error
            
        set_value('PM (10, 25, 100): {0}, {1}, {2}'.format(*pm))
