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
4. Kalibriere magnetischen Fluss:
    * Bewege Compass Bricklet in jede Richtung bis min/max sich nicht mehr ändern. Stelle sicher, dass keine Magnetfeldquellen in der Nähe des Bricklets sind. Drücke Kalibrieren wenn fertig.
5. Überprüfe Ausrichtung: Drehe bis 0° (Nord), 90° (Ost), 180° (Süd), 270° (West)
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_flux_density = None
        self.reached_negative = False
        self.reached_positive = False
        self.calibrated = False
        self.x = [0, 0, 0]
        self.y = [0, 0, 0]
        self.z = [0, 0, 0]

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_flux_density != None:
            self.cbe_flux_density.set_period(0)
        l = self.mw.compass_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

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

        l = self.mw.compass_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)
        self.mw.button_calibration_remove.setVisible(False)
        self.mw.button_calibration_save.clicked.connect(self.calibration_save_clicked)
        self.mw.button_calibration_remove.clicked.connect(self.calibration_remove_clicked)


        self.reset_calibration()

        self.cbe_flux_density = CallbackEmulator(self.compass.get_magnetic_flux_density,
                                             self.cb_mfd,
                                             ignore_last_data=True)
        self.cbe_flux_density.set_period(20)


        self.show_device_information(device_information)

    def reset_calibration(self):
        self.x = [0, 0, 0]
        self.y = [0, 0, 0]
        self.z = [0, 0, 0]

        off = [0]*3
        mul = [10000]*3
        self.compass.set_calibration(off, mul)
        self.calibrated = False

    def calibration_remove_clicked(self):
        self.reset_calibration()
        l = self.mw.compass_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)
        self.mw.button_calibration_remove.setVisible(False)

    def calibration_save_clicked(self):
        off = [0]*3
        mul = [10000]*3

        off[0] = int(round((self.x[1] + self.x[2])/2, 0))
        off[1] = int(round((self.y[1] + self.y[2])/2, 0))
        off[2] = int(round((self.z[1] + self.z[2])/2, 0))

        mul[0] = 10000
        mul[1] = int(round(10000*(abs(self.x[1]) + abs(self.x[2]))/(abs(self.y[1]) + abs(self.y[2])), 0))
        mul[2] = int(round(10000*(abs(self.x[1]) + abs(self.x[2]))/(abs(self.z[1]) + abs(self.z[2])), 0))

        self.compass.set_calibration(off, mul)
        l = self.mw.compass_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)
        self.mw.button_calibration_remove.setVisible(True)
        self.calibrated = True

    def update_calibration_labels(self):
        self.x[1] = min(self.x[0], self.x[1])
        self.x[2] = max(self.x[0], self.x[2])
        self.y[1] = min(self.y[0], self.y[1])
        self.y[2] = max(self.y[0], self.y[2])
        self.z[1] = min(self.z[0], self.z[1])
        self.z[2] = max(self.z[0], self.z[2])

        self.mw.label_x_cur.setText('{0}'.format(self.x[0]))
        self.mw.label_y_cur.setText('{0}'.format(self.y[0]))
        self.mw.label_z_cur.setText('{0}'.format(self.z[0]))

        self.mw.label_x_min.setText('{0}'.format(self.x[1]))
        self.mw.label_y_min.setText('{0}'.format(self.y[1]))
        self.mw.label_z_min.setText('{0}'.format(self.z[1]))

        self.mw.label_x_max.setText('{0}'.format(self.x[2]))
        self.mw.label_y_max.setText('{0}'.format(self.y[2]))
        self.mw.label_z_max.setText('{0}'.format(self.z[2]))

    def calibrate(self, data):
        x, y, z = data
        self.x[0] = x
        self.y[0] = y
        self.z[0] = z

        self.update_calibration_labels()

    def cb_mfd(self, data):
        if not self.calibrated:
            self.mw.set_value_action('Kalibrieren')
            self.calibrate(data)
            return

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

        heading_str = 'Ausrichtung: {}°\n'.format(heading)
        for i, name in enumerate(['Nord', 'Ost', 'Süd', 'West']):
            heading_str += '\t{} {}° ({})\n'.format(reached if self.headings_reached[i] else not_reached,
                                                  i * 90,
                                                  name)

        if all(self.headings_reached):
            self.mw.set_value_okay(heading_str)
        else:
            self.mw.set_value_action(heading_str)
