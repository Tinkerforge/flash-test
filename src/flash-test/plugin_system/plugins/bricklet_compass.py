# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

bricklet_compass.py: Compass plugin

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

from ..tinkerforge.bricklet_compass import BrickletCompass
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Compass Bricklet  mit Flash Adapter XMC
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Heading: Drehe bis 0° (Nord), 90° (Ost), 180° (Süd), 270° (West)
5. Das Bricklet ist fertig, zusammen mit Knopf in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_flux_density = None
        self.reached_negative = False
        self.reached_positive = False

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_flux_density != None:
            self.cbe_flux_density.set_period(0)

    def get_device_identifier(self):
        return BrickletCompass.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletCompass.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_flux_density != None:
            self.cbe_flux_density.set_period(0)

        self.headings_reached = [False, False, False, False] #North, East, South, West

        self.compass = BrickletCompass(device_information.uid, self.get_ipcon())
        if self.compass.get_bootloader_mode() != BrickletCompass.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_flux_density = CallbackEmulator(self.compass.get_magnetic_flux_density,
                                             self.cb_mfd,
                                             ignore_last_data=True)
        self.cbe_flux_density.set_period(25)

        self.show_device_information(device_information)

    def cb_mfd(self, data):
        def near(x, y):
            return abs(y-x) < 3

        x, y, z = data
        heading = int(round(math.atan2(y, x)*180/math.pi, 0))
        if heading < 0:
            heading += 360

        for i in range(0, 4):
            if near(heading, i * 90):
                self.headings_reached[i] = True

        not_reached = '\u25C7'
        reached = '\u25C6'

        heading_str = 'Current heading: {}°\n'.format(heading)
        for i, name in enumerate(['Nord', 'Ost', 'Süd', 'West']):
            heading_str += '\t{} {}° ({})\n'.format(reached if self.headings_reached[i] else not_reached,
                                                  i * 90,
                                                  name)

        if all(self.headings_reached):
            self.mw.set_value_okay(heading_str)
        else:
            self.mw.set_value_action(heading_str)
