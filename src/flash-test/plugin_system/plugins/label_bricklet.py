# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2022 Matthias Bolte <matthias@tinkerforge.com>

label_bricklet.py: Bricklet label print plugin

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
from PyQt5.QtWidgets import QMessageBox

from ..util import LabelInfo
from ..plugin_base import PluginBase
from ..tinkerforge.bricklet_distance_ir_v2 import BrickletDistanceIRV2
from ..tinkerforge.bricklet_e_paper_296x128 import BrickletEPaper296x128

import traceback

class Plugin(PluginBase):
    TODO_TEXT = u"""\
1. Verbinde fertiges Bricklet mit Master Brick 3.0
2. Etikett wird automatisch gedruckt
"""

    def start(self):
        self.mw.button_flash.setEnabled(False)
        self.mw.check_print_label.show()
        self.mw.button_continue.hide()
        PluginBase.start(self)
        self.show_device_information(None, clear_value=True)

    def show_device_information(self, device_information, clear_value=False):
        if device_information != None:
            self.mw.set_tool_status_okay("Plugin gefunden")

            if device_information.uid in ['1', '7xwQ9g']:
                self.mw.set_uid_status_error("Aktuelle UID " + device_information.uid + " ist ungültig")
            else:
                self.mw.set_uid_status_okay("Aktuelle UID lautet " + device_information.uid)

            self.mw.set_flash_status_okay("Aktuelle Firmware Version lautet " + '.'.join([str(fw) for fw in device_information.firmware_version]))
        else:
            self.mw.set_tool_status_normal("Kein Plugin gefunden")
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')

        if clear_value:
            self.mw.set_value_normal('-')

    def handles_device_identifier(self, device_identifier):
        return str(device_identifier).startswith('2')

    def new_enum(self, device_information):
        self.show_device_information(device_information)

        if self.mw.check_print_label.isChecked():
            sku = device_information.device_identifier

            if sku == BrickletDistanceIRV2.DEVICE_IDENTIFIER:
                sensor_type = BrickletDistanceIRV2(device_information.uid, self.get_ipcon()).get_sensor_type()

                if sensor_type == 0:
                    sku = 2125 # 4-30cm
                elif sensor_type == 1:
                    sku = 2142 # 10-80cm
                elif sensor_type == 2:
                    sku = 2143 # 20-150cm
                else:
                    QMessageBox.critical(self.mw, 'Distance IR Bricklet 2.0', 'Unbekannter Sharp Distanz-Sensor: {0}'.format(sensor_type))
                    return

            elif sku == BrickletEPaper296x128.DEVICE_IDENTIFIER:
                color = BrickletEPaper296x128(device_information.uid, self.get_ipcon()).get_display_type()

                if color == 0:
                    sku = 2146 # red
                elif color == 1:
                    sku = 2148 # gray
                else:
                    QMessageBox.critical(self.mw, 'E-Paper 296x128 Bricklet', 'Unbekannte Farbe: {0}'.format(color))
                    return

            self.mw.print_label(LabelInfo(sku, device_information.uid, device_information.firmware_version, device_information.hardware_version))
