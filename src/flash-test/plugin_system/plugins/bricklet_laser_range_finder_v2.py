# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_laser_range_finder_v2.py: Laser Range Finder 2.0 plugin

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

from ..tinkerforge.bricklet_laser_range_finder_v2 import BrickletLaserRangeFinderV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Laser Range Finder Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Wert (z.B. ~2m zur Decke)
5. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_distance = None

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        super().stop()
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

    def get_device_identifier(self):
        return BrickletLaserRangeFinderV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletLaserRangeFinderV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

        self.laser_range_finder = BrickletLaserRangeFinderV2(device_information.uid, self.get_ipcon())
        if self.laser_range_finder.get_bootloader_mode() != BrickletLaserRangeFinderV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_distance = CallbackEmulator(self.laser_range_finder.get_distance, self.cb_distance)
        self.cbe_distance.set_period(100)

        self.laser_range_finder.enable_laser() # FIXME: Use correct new API

        self.show_device_information(device_information)

    def cb_distance(self, distance):
        self.mw.set_value_normal('Entfernung: ' + str(distance) + ' cm')
