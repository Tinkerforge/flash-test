# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_voltage_current_v2_v2.py: Voltage/Current 2.0 plugin

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

from ..tinkerforge.bricklet_voltage_current_v2 import BrickletVoltageCurrentV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Voltage/Current Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Kalibriere Strom:
   * Schließe Testaufbau (24V/1A) an
   * Überprüfe Anzeige = ~24V/1A
   * Trage mit Multimeter gemessenen Strom ein und drücke 'Kalibrieren'
5. Das Bricklet ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_voltage = None
        self.cbe_current = None
        self.last_values = [0, 0]

    def start(self):
        CoMCUBrickletBase.start(self)

        self.mw.button_save_vc.clicked.connect(self.save_clicked)


    def stop(self):
        super().stop()
        self.mw.button_save_vc.clicked.disconnect(self.save_clicked)

        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)
        if self.cbe_current != None:
            self.cbe_current.set_period(0)

        l = self.mw.voltage_current_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

    def get_device_identifier(self):
        return BrickletVoltageCurrentV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletVoltageCurrentV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_voltage != None:
            self.cbe_voltage.set_period(0)
        if self.cbe_current != None:
            self.cbe_current.set_period(0)

        l = self.mw.voltage_current_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)

        self.voltage_current_v2 = BrickletVoltageCurrentV2(device_information.uid, self.get_ipcon())
        if self.voltage_current_v2.get_bootloader_mode() != BrickletVoltageCurrentV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_voltage = CallbackEmulator(lambda: self.voltage_current_v2.get_voltage(), self.cb_voltage)
        self.cbe_voltage.set_period(100)

        self.cbe_current = CallbackEmulator(lambda: self.voltage_current_v2.get_current(), self.cb_current)
        self.cbe_current.set_period(100)

        self.show_device_information(device_information)

    def cb_voltage(self, voltage):
        self.last_values[0] = voltage/1000.0
        self.mw.set_value_normal('Spannung: ' + str(self.last_values[0]) +  ' V, Strom: ' + str(self.last_values[1]) + ' A')

    def cb_current(self, current):
        self.last_values[1] = current/1000.0
        self.mw.set_value_normal('Spannung: ' + str(self.last_values[0]) +  ' V, Strom: ' + str(self.last_values[1]) + ' A')

    def save_clicked(self):
        self.mw.set_tool_status_action('Kalibriere... ')
        QtWidgets.QApplication.processEvents()

        self.voltage_current_v2.set_calibration(1, 1, 1, 1)

        time.sleep(0.5)

        current_device = self.voltage_current_v2.get_current()
        current_real   = self.mw.spinbox_current_vc.value()

        self.voltage_current_v2.set_calibration(1, 1, current_real, current_device)

        self.mw.set_tool_status_okay('Kalibrierung OK: ' + str(current_device) + '/' + str(current_real))
