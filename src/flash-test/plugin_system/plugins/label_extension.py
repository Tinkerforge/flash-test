# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2022 Matthias Bolte <matthias@tinkerforge.com>

label_extension.py: Extension label print plugin

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

from PyQt5 import Qt, QtGui, QtCore, QtWidgets

from ..util import LabelInfo
from ..plugin_base import PluginBase
from ..tinkerforge.brick_master import BrickMaster

import time

class Plugin(PluginBase):
    TODO_TEXT = u"""\
1. Stecke fertige Extension auf Master Brick
2. Stecke Master Brick an USB
2. Etikett wird automatisch gedruckt
"""

    def start(self):
        self.mw.button_flash.setEnabled(False)
        self.mw.check_print_label.show()
        self.mw.button_continue.hide()
        PluginBase.start(self)
        self.mw.set_tool_status_okay("-")
        self.mw.set_uid_status_okay("-")
        self.mw.set_flash_status_okay("-")
        self.mw.set_value_normal('-')

    def handles_device_identifier(self, device_identifier):
        return device_identifier == BrickMaster.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        master = BrickMaster(device_information.uid, self.get_ipcon())

        self.mw.set_tool_status_normal('Master Brick gefunden')

        for x in range(10):
            QtWidgets.QApplication.processEvents()
            time.sleep(0.01)

        firmware_version = '-'

        if master.is_chibi_present():
            sku = 31
            name = 'Chibi Extension'
        elif master.is_rs485_present():
            sku = 32
            name = 'RS485 Extension'
        elif master.is_wifi_present():
            sku = 33
            name = 'WIFI Extension'
        elif master.is_ethernet_present():
            self.mw.set_tool_status_okay('Ethernet Extension gefunden')

            mbox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, 'Ethernet Extension', 'Hat die angeschlossene Ethernet Extension PoE?', parent=self.mw)
            with_poe_button = mbox.addButton('Mit PoE', QtWidgets.QMessageBox.YesRole)
            without_poe_button = mbox.addButton('Ohne PoE', QtWidgets.QMessageBox.NoRole)
            mbox.addButton('Abbrechen', QtWidgets.QMessageBox.RejectRole)

            mbox.exec_()
            clicked_button = mbox.clickedButton()

            if clicked_button == with_poe_button:
                sku = 34
                name = 'Ethernet Extension (mit PoE)'
            elif clicked_button == without_poe_button:
                sku = 35
                name = 'Ethernet Extension (ohne PoE)'
            else:
                return
        elif master.is_wifi2_present():
            sku = 36
            name = 'WIFI Extension 2.0'
            firmware_version = master.get_wifi2_firmware_version()
        else:
            self.mw.set_tool_status_error("Keine Extension gefunden")
            return

        status = name + ' gefunden'

        if firmware_version != '-':
            status += ', FW Version: ' + '.'.join([str(x) for x in firmware_version])

        self.mw.set_tool_status_okay(status)

        if self.mw.check_print_label.isChecked():
            self.mw.print_label(LabelInfo(sku, '-', firmware_version))
