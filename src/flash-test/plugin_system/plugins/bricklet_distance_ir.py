# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_distance_ir.py: Distance IR plugin

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

from PyQt5 import Qt, QtWidgets, QtCore

from ..tinkerforge.bricklet_distance_ir import BrickletDistanceIR
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math
import os

# this class is directly based on the QwtSpline class from the Qwt library
class NaturalSpline(object):
    def __init__(self):
        self.points = []
        self.a = []
        self.b = []
        self.c = []

    def set_points(self, points):
        length = len(points)

        if length < 3:
            return False

        a = [0.0] * (length - 1)
        b = [0.0] * (length - 1)
        c = [0.0] * (length - 1)
        h = [0.0] * (length - 1)

        for i in range(length - 1):
            h[i] = points[i + 1][0] - points[i][0]

            if h[i] <= 0:
                return False

        d = [0.0] * (length - 1)
        dy1 = (points[1][1] - points[0][1]) / h[0]

        for i in range(1, length - 1):
            c[i] = h[i]
            b[i] = h[i]
            a[i] = 2.0 * (h[i - 1] + h[i])
            dy2 = (points[i + 1][1] - points[i][1]) / h[i]
            d[i] = 6.0 * (dy1 - dy2)
            dy1 = dy2

        for i in range(1, length - 2):
            c[i] /= a[i]
            a[i + 1] -= b[i] * c[i]

        s = [0.0] * length
        s[1] = d[1]

        for i in range(2, length - 1):
            s[i] = d[i] - c[i - 1] * s[i - 1]

        s[length - 2] = -s[length - 2] / a[length - 2]

        for i in reversed(range(1, length - 2)):
            s[i] = - ( s[i] + b[i] * s[i+1] ) / a[i]

        s[length - 1] = s[0] = 0.0

        for i in range(length - 1):
            a[i] = (s[i+1] - s[i]) / (6.0 * h[i])
            b[i] = 0.5 * s[i]
            c[i] = (points[i+1][1] - points[i][1]) / h[i] - (s[i + 1] + 2.0 * s[i]) * h[i] / 6.0

        self.points = points
        self.a = a
        self.b = b
        self.c = c

        return True

    def get_index(self, x):
        points = self.points
        length = len(points)

        if x <= points[0][0]:
            i1 = 0
        elif x >= points[length - 2][0]:
            i1 = length - 2
        else:
            i1 = 0
            i2 = length - 2
            i3 = 0

            while i2 - i1 > 1:
                i3 = i1 + ((i2 - i1) >> 1)

                if points[i3][0] > x:
                    i2 = i3
                else:
                    i1 = i3

        return i1

    def get_value(self, x):
        if len(self.a) == 0:
            return 0.0

        i = self.get_index(x)
        delta = x - self.points[i][0]

        return (((self.a[i] * delta) + self.b[i]) * delta + self.c[i]) * delta + self.points[i][1]

class Plugin(BrickletBase):
    NUM_VALUES = 128
    DIVIDER = 2**12//NUM_VALUES

    TODO_TEXT = u"""\
0. Wähle korrekten Sensor aus
1. Verbinde Distance IR Bricklet (inklusive Sensor) mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Kalibrierung wird geflasht, danach startet Master Brick nochmal neu
5. Entfernung wird angezeigt, überprüfe Entfernung.
6. Das Bricklet ist fertig, mit Sensor in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_distance = None
        self.calibrated = False

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

        l = self.mw.distance_ir_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)

    def stop(self):
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

        l = self.mw.distance_ir_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

    def get_device_identifier(self):
        return BrickletDistanceIR.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletDistanceIR.DEVICE_URL_PART))
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

    def new_enum(self, device_information):
        if self.cbe_distance != None:
            self.cbe_distance.set_period(0)

        self.show_device_information(device_information)

        self.distance_ir = BrickletDistanceIR(device_information.uid, self.get_ipcon())
        if not self.calibrated:
            self.calibrated = True
            self.write_calibration()
            self.master_reset()
        else:
            self.calibrated = False
            self.cbe_distance = CallbackEmulator(self.distance_ir.get_distance, self.cb_distance)
            self.cbe_distance.set_period(100)

    def cb_distance(self, distance):
        self.mw.set_value_normal('Entfernung: ' + str(distance/10) +  'cm')

    def sample_interpolate(self, x, y):
        spline = NaturalSpline()
        points = []

        for point in zip(x, y):
            points.append((float(point[0]), float(point[1])))

        spline.set_points(points)

        px = range(0, 2**12, Plugin.DIVIDER)
        py = []

        for X in px:
            py.append(spline.get_value(X))

        for i in range(x[0]//Plugin.DIVIDER):
            py[i] = y[0]

        for i in range(x[-1]//Plugin.DIVIDER, 2**12//Plugin.DIVIDER):
            py[i] = y[-1]

        for i in range(len(py)):
            if py[i] > y[0]:
                py[i] = y[0]
            if py[i] < y[-1]:
                py[i] = y[-1]

        try:
            self.distance_ir.set_response_expected(BrickletDistanceIR.FUNCTION_SET_SAMPLING_POINT, True)
            for i in range(Plugin.NUM_VALUES):
                value = int(round(py[i]*100))
                self.distance_ir.set_sampling_point(i, value)
                self.mw.set_value_normal("Writing sample point {0} with value {1} ".format(i, value))
        except:
            import traceback
            traceback.print_exc()
            return

    def write_calibration(self):
        x = []
        y = []
        index = self.mw.distance_ir_sensor_combo.currentIndex()
        if index == 0:
            filename = '2D120.txt'
        elif index == 1:
            filename = '2Y0A02.txt'
        elif index == 2:
            filename = '2Y0A21.txt'
        elif index == 3:
            filename = 'A41SK.txt'

        file_directory = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(file_directory, '..', '..', '..', '..', 'calibrations', filename)

        with open(file, 'r') as f:
            for line in f:
                c = line.find('#')
                if c != -1:
                    line = line[:c]

                line = line.strip()

                if line.startswith('\xEF\xBB\xBF'): # strip UTF-8 BOM, Internet Explorer adds it to text files
                    line = line[3:]

                if len(line) == 0:
                    continue

                if ':' not in line:
                    QtWidgets.QMessageBox.critical(get_main_window(), "Sample points",
                                               "Sample points file is malformed (error code 1)",
                                               QtWidgets.QMessageBox.Ok)
                    return

                s = line.split(':')

                if len(s) != 2:
                    QtWidgets.QMessageBox.critical(get_main_window(), "Sample points",
                                               "Sample points file is malformed (error code 2)",
                                               QtWidgets.QMessageBox.Ok)
                    return

                try:
                    x.append(int(s[1]))
                    y.append(int(s[0]))
                except:
                    QtWidgets.QMessageBox.critical(get_main_window(), "Sample points",
                                               "Sample points file is malformed (error code 3)",
                                               QtWidgets.QMessageBox.Ok)
                    return

        self.sample_interpolate(x, y)
