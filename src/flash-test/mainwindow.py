# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

mainwindow.py: Flash and test tool main window

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

from PyQt4 import Qt, QtGui, QtCore

from ui_mainwindow import Ui_MainWindow
from device_manager import DeviceManager
from plugin_system.plugin_base import PluginBase
from plugin_system.tinkerforge.brick_master import BrickMaster

import urllib.request
import sys
import os

class PluginNotImplemented(PluginBase):
    pass

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        try:
            file_directory = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(file_directory, '..', '..', 'staging_password.txt'), 'rb') as f:
                staging_password = f.read().decode('utf-8').split('\n')[0].strip()
        except:
            QtGui.QMessageBox.critical(None, 'Error', 'staging_password.txt missing or malformed')
            sys.exit(0)

        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='Staging area',
                                  uri='http://stagingwww.tinkerforge.com/uid',
                                  user='staging',
                                  passwd=staging_password)
        opener = urllib.request.build_opener(auth_handler)
        urllib.request.install_opener(opener)

        self.setupUi(self)
        self.current_plugin = None
        self.device_manager = DeviceManager(self)
        self.plugin_not_implemented = PluginNotImplemented(self)

        from device_identifiers import device_identifiers
        from plugin_system.device_classes import device_classes

        self.device_by_identifier = {}
        for cls in device_classes:
            instance = cls(self)
            self.device_by_identifier[instance.get_device_identifier()] = instance

        for di in sorted(device_identifiers, key=lambda x: x[1]):
            name = di[1]
            device_identifier = di[0]
            self.combo_device.addItem(name, self.device_by_identifier.get(device_identifier))

        self.combo_device.currentIndexChanged.connect(self.device_index_changed)
        self.button_flash.clicked.connect(self.flash_clicked)

    def closeEvent(self, event):
        if self.current_plugin:
            self.current_plugin.stop()
            self.current_plugin.destroy()

        os._exit(0)

    def get_master_brick_device_information(self):
        return self.device_manager.devices.get(BrickMaster.DEVICE_IDENTIFIER)

    def device_index_changed(self, index):
        if self.current_plugin:
            self.current_plugin.stop()

        device = self.combo_device.itemData(index)
        if device:
            self.current_plugin = device
            device_information = self.device_manager.devices.get(device.get_device_identifier())
        else:
            self.current_plugin = self.plugin_not_implemented
            device_information = None

        self.current_plugin.start(device_information)

    def flash_clicked(self):
        if self.current_plugin:
            self.current_plugin.flash_clicked()
