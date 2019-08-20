# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

bricklet_energy_monitor.py: Energy Monitor plugin

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

import time

from ..tinkerforge.bricklet_energy_monitor import BrickletEnergyMonitor
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Energy Monitor Bricklet mit Flash Adapter XMC
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Stecke beide Kalibrierungsadapter ein
5. Warte auf Kalibrierung
6. Stecke echten Spannungstranformator und Stromwandler ein
7. Prüfe Messwerte. Wenn grün, dann weiter
8. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
9. Gehe zu 1
"""

    VOLTAGE_LOWER_BOUND = 210
    VOLTAGE_UPPER_BOUND = 240

    FREQUENCY_LOWER_BOUND = 45
    FREQUENCY_UPPER_BOUND = 55

    CURRENT_LOWER_BOUND = 0.35
    CURRENT_UPPER_BOUND = 1.15

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_energy_data = None
        self.cbe_transformer_status = None

    def start(self):
        CoMCUBrickletBase.start(self)
        self.mw.label_value.setTextFormat(QtCore.Qt.RichText)

    def stop(self):
        super().stop()
        self.mw.label_value.setTextFormat(QtCore.Qt.AutoText)
        if self.cbe_energy_data != None:
            self.cbe_energy_data.set_period(0)

        if self.cbe_transformer_status != None:
            self.cbe_transformer_status.set_period(0)

    def get_device_identifier(self):
        return BrickletEnergyMonitor.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletEnergyMonitor.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_energy_data != None:
            self.cbe_energy_data.set_period(0)

        if self.cbe_transformer_status != None:
            self.cbe_transformer_status.set_period(0)

        self.voltage_transformer_connected = False
        self.current_transformer_connected = False
        self.calibration_state = 0
        self.calibration_time = 0

        self.em = BrickletEnergyMonitor(device_information.uid, self.get_ipcon())
        if self.em.get_bootloader_mode() != BrickletEnergyMonitor.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_energy_data = CallbackEmulator(lambda: self.em.get_energy_data(), self.cb_energy_data, ignore_last_data=True)
        self.cbe_energy_data.set_period(100)

        self.cbe_transformer_status = CallbackEmulator(lambda: self.em.get_transformer_status(), self.cb_transformer_status, ignore_last_data=True)
        self.cbe_transformer_status.set_period(100)

        self.show_device_information(device_information)

    def cb_energy_data(self, data):
        voltage, current, energy, real_power, apparent_power, reactive_power, power_factor, frequency = data

        value_string = 'V: {}mV, C: {}mA, E: {}mWh\nRP: {}mW, AP: {}mVA, RP: {}mVAR\nPF: {:03}, F: {}Hz'
        value_string = value_string.format(voltage * 10,
                                           current * 10,
                                           energy * 10,
                                           real_power * 10,
                                           apparent_power * 10,
                                           reactive_power * 10,
                                           power_factor / 1000.0,
                                           frequency / 100)

        voltage_dev_name = 'Spannungskalibrierungsadapter' if self.calibration_state < 4 else 'Spannungstransformator'
        current_dev_name = 'Stromkalibrierungsadapter' if self.calibration_state < 4 else 'Stromwandler'

        connection_string = '{} {}angeschlossen.<br/>{} {}angeschlossen.'
        connection_string = connection_string.format(voltage_dev_name,
                                                     '' if self.voltage_transformer_connected else '<span style="color:red;">nicht</span> ',
                                                     current_dev_name,
                                                     '' if self.current_transformer_connected else '<span style="color:red;">nicht</span> ')

        if self.calibration_state == 0:
            cal_string = '<span style="color:red;">Warte auf Kalibrierungsadapter.</span>'
        elif self.calibration_state == 1:
            cal_string = 'Kalibrierung läuft.'
        elif self.calibration_state == 2:
            cal_string = 'Kalibrierung wird gespeichert.'
        elif self.calibration_state in [3, 4]:
            cal_string = '<span style="color:green;">Kalibrierung abgeschlossen.</span> <span style="color:red;">Warte auf Spannungstransformator und Stromwandler</span>'
        elif self.calibration_state == 5:
            cal_string = '<span style="color:green;">Kalibrierung abgeschlossen.</span> Prüfe Messwerte'

        if self.calibration_state == 5:
            voltage_okay = self.VOLTAGE_LOWER_BOUND < voltage / 100.0 < self.VOLTAGE_UPPER_BOUND
            current_okay = self.CURRENT_LOWER_BOUND < current / 100.0 < self.CURRENT_UPPER_BOUND
            frequency_okay = self.FREQUENCY_LOWER_BOUND < frequency / 100.0 < self.FREQUENCY_UPPER_BOUND
            if voltage_okay and current_okay and frequency_okay:
                value_string = '<span style="color:green;">' + value_string + '</span>'
            else:
                value_string = '<span style="color:red;">' + value_string + '</span>'


        self.mw.set_value_normal('<br/>'.join([connection_string, cal_string, value_string]))

    def cb_transformer_status(self, status):
        self.voltage_transformer_connected, self.current_transformer_connected = status
        if self.calibration_state == 0 and status == (True, True):
            self.calibration_state = 1
            self.calibration_time = time.time()
        elif self.calibration_state == 1 and  time.time() - self.calibration_time > 0.5:
            self.calibration_state = 2
            self.em.calibrate_offset()
            self.calibration_state = 3
        elif self.calibration_state == 3 and status != (True, True):
            self.calibration_state = 4
        elif self.calibration_state == 4 and status == (True, True):
            self.calibration_state = 5
