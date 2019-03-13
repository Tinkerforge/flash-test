# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_industrial_dual_analog_in.py: Industrial Dual Analog In plugin

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

from ..tinkerforge.bricklet_industrial_dual_analog_in import BrickletIndustrialDualAnalogIn
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import math

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Industrial Dual Analog In Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Kalibriere Spannung:
   * Schließe Testadapter 1 an (zwei Brücken) -> Drücke 'Offset'
   * Überprüfe Anzeige = 0V
   * Schließe Testadapter 2 an (Netzteil) -> Drücke 'Gain'
   * Überprüfe Anzeige = ~24V
   * Überprüfe Drittspannung
5. Das Bricklet ist fertig, mit grünem 8-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)
        self.cbe_voltage0 = None
        self.cbe_voltage1 = None
        self.last_voltage = [0, 0]

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        self.mw.button_offset_idai.clicked.connect(self.offset_clicked)
        self.mw.button_gain_idai.clicked.connect(self.gain_clicked)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        self.mw.button_offset_idai.clicked.disconnect(self.offset_clicked)
        self.mw.button_gain_idai.clicked.disconnect(self.gain_clicked)

        if self.cbe_voltage0 != None:
            self.cbe_voltage0.set_period(0)
        if self.cbe_voltage1 != None:
            self.cbe_voltage1.set_period(0)

        l = self.mw.industrial_dual_analog_in_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

    def get_device_identifier(self):
        return BrickletIndustrialDualAnalogIn.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletIndustrialDualAnalogIn.DEVICE_URL_PART))

    def new_enum(self, device_information):
        if self.cbe_voltage0 != None:
            self.cbe_voltage0.set_period(0)
        if self.cbe_voltage1 != None:
            self.cbe_voltage1.set_period(0)

        l = self.mw.industrial_dual_analog_in_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)

        self.industrial_dual_analog_in = BrickletIndustrialDualAnalogIn(device_information.uid, self.get_ipcon())
        self.cbe_voltage0 = CallbackEmulator(lambda: self.industrial_dual_analog_in.get_voltage(0),
                                             lambda v: self.cb_voltage(0, v))
        self.cbe_voltage0.set_period(100)

        self.cbe_voltage1 = CallbackEmulator(lambda: self.industrial_dual_analog_in.get_voltage(1),
                                             lambda v: self.cb_voltage(1, v))
        self.cbe_voltage1.set_period(100)

        self.show_device_information(device_information)

    def cb_voltage(self, channel, voltage):
        self.last_voltage[channel] = voltage/1000.0
        self.mw.set_value_normal('Spannung Kanal 0: ' + str(self.last_voltage[0]) + ' V, Kanal 1: ' + str(self.last_voltage[1]) + ' V')

    def offset_clicked(self):
        self.mw.set_tool_status_action('Kalibriere Offset... ')
        self.industrial_dual_analog_in.set_calibration((0, 0), (0, 0))
        time.sleep(0.5)
        adc0 = 0
        adc1 = 0
        for i in range(10):
            adcs = self.industrial_dual_analog_in.get_adc_values()
            adc0 += adcs[0]
            adc1 += adcs[1]
            time.sleep(0.1)
        self.industrial_dual_analog_in.set_calibration((-adc0//10, -adc1//10), (0, 0))

        self.mw.set_tool_status_okay('Kalibrierung OK: ' + str((-adc0//10, -adc1//10)))

    def gain_clicked(self):
        self.mw.set_tool_status_action('Kalibriere Gain... ')
        old_cal = self.industrial_dual_analog_in.get_calibration()

        adc0 = 0
        adc1 = 0
        for i in range(10):
            adcs = self.industrial_dual_analog_in.get_adc_values()
            adc0 += adcs[0]
            adc1 += adcs[1]
            time.sleep(0.1)

        measured0 = (adc0/10.0)*244/44983
        measured1 = (adc1/10.0)*244/44983
        factor0 = self.mw.spinbox_voltage_idai.value()/measured0
        factor1 = self.mw.spinbox_voltage_idai.value()/measured1
        gain0 = int((factor0-1)*2**23)
        gain1 = int((factor1-1)*2**23)

        def is_int32(value):
            return value >= -2147483648 and value <= 2147483647

        if not is_int32(gain0) or not is_int32(gain1):
            self.mw.set_tool_status_error('Kalibrierung außerhalb des möglichen Bereiches: ' + str((gain0, gain1)))
            return

        self.industrial_dual_analog_in.set_calibration((old_cal.offset[0], old_cal.offset[1]), (gain0, gain1))

        self.mw.set_tool_status_okay('Kalibrierung OK: ' + str((gain0, gain1)))
