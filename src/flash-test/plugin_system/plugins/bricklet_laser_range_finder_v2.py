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

import time

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Laser Range Finder Bricklet 2.0 mit Port C
2. Stelle Bricklet fest auf tisch (guckt zur Decke), nicht wackeln während Kalibrierung! 
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Bricklet Kalibriert sich (dauert ca. 1s)
6. Überprüfe Wert (ca. 180cm zur Decke)
7. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_distance = None
        self.offset = 0

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


        self.mw.set_value_normal('Kalibriere...')
        self.laser_range_finder.set_enable(True)
        time.sleep(0.25)
        self.laser_range_finder.set_offset_calibration(0)
        self.laser_range_finder.set_configuration(128, True, 1, 10)
        time.sleep(0.25)

        velocity_sum = 0
        for i in range(10):
            time.sleep(0.1)
            velocity_sum += self.laser_range_finder.get_velocity()

        self.offset = int(round(velocity_sum/100, 0))
        self.laser_range_finder.set_offset_calibration(self.offset)

        self.cbe_distance = CallbackEmulator(self.laser_range_finder.get_distance, self.cb_distance)
        self.cbe_distance.set_period(100)

        self.show_device_information(device_information)

    def cb_distance(self, distance):
        self.mw.set_value_normal('Offset: {0}, Entfernung: {1} cm'.format(self.offset, distance))
