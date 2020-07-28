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

from PyQt5 import Qt, QtGui, QtCore, QtWidgets

from ui_mainwindow import Ui_MainWindow
from device_manager import DeviceManager
from plugin_system.plugin_base import PluginBase
from plugin_system.tinkerforge.brick_master import BrickMaster

import urllib.request
import sys
import os
import ssl

class PluginNotImplemented(PluginBase):
    pass

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    qtcb_foot_pedal = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        try:
            file_directory = os.path.dirname(os.path.realpath(__file__))
            with open(os.path.join(file_directory, '..', '..', 'staging_password.txt'), 'rb') as f:
                staging_password = f.read().decode('utf-8').split('\n')[0].strip()
        except:
            QtWidgets.QMessageBox.critical(None, 'Error', 'staging_password.txt missing or malformed')
            sys.exit(0)

        context = ssl.SSLContext(protocol=PROTOCOL_TLS)
        #context.verify_mode = ssl.CERT_REQUIRED
        #context.load_verify_locations(certifi.where())
        https_handler = urllib.request.HTTPSHandler(context=context)

        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(realm='Staging',
                                  uri='https://stagingwww.tinkerforge.com',
                                  user='staging',
                                  passwd=staging_password)

        opener = urllib.request.build_opener(https_handler, auth_handler)
        urllib.request.install_opener(opener)

        self.setupUi(self)
        self.resize(800, 800)
        temp_layouts = [self.industrial_dual_analog_in_layout,
                        self.voltage_current_layout,
                        self.distance_ir_layout,
                        self.ethernet_extension_layout,
                        self.color_layout,
                        self.piezo_speaker_layout,
                        self.multi_touch_layout,
                        self.compass_layout]
        for l in temp_layouts:
            self.hide_layout(l)

        self.foot_pedal = None
        self.current_plugin = None
        self.device_manager = DeviceManager(self)
        self.plugin_not_implemented = PluginNotImplemented(self)

        from plugin_system.tinkerforge.device_factory_all import DEVICE_CLASSES
        from plugin_system.device_classes import device_classes

        device_identifiers = []

        for key, value in DEVICE_CLASSES.items():
            device_identifiers.append((key, value.DEVICE_DISPLAY_NAME))

        device_identifiers.append((10013, 'Chibi Extension'))
        device_identifiers.append((20013, 'RS485 Extension'))
        device_identifiers.append((30013, 'WIFI Extension'))
        device_identifiers.append((40013, 'Ethernet Extension'))
        device_identifiers.append((50013, 'WIFI Extension 2.0'))

        device_identifiers.append((102, 'Smartbed Brick'))

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
        self.button_restart_test.clicked.connect(self.restart_test_clicked)
        self.button_continue.clicked.connect(self.continue_clicked)

        self.flash_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_0), self, self.flash_clicked)
        self.flash_shortcut.setAutoRepeat(False)

        self.button_continue.hide()

        self.device_index_changed(0)

        self.qtcb_foot_pedal.connect(self.cb_foot_pedal)

        self.flashed_count = 0

    def cb_foot_pedal(self, interrupt_mask, value_mask):
        if (interrupt_mask & 1) != 0 and (value_mask & 1) == 0:
            self.flash_clicked()

    def hide_layout(self, l):
        for i in range(l.count()):
            item = l.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setVisible(False)

    def show_layout(self, l):
        for i in range(l.count()):
            item = l.itemAt(i)
            widget = item.widget()
            if widget:
                widget.setVisible(True)

    def closeEvent(self, event):
        if self.current_plugin != None:
            self.current_plugin.stop()
            self.current_plugin.destroy()

        os._exit(0)

    def get_master_brick_device_information(self):
        return self.device_manager.devices.get(BrickMaster.DEVICE_IDENTIFIER)

    def device_index_changed(self, index):
        if self.current_plugin != None:
            self.current_plugin.stop()

        device = self.combo_device.itemData(index)

        if device != None:
            self.current_plugin = device
        else:
            self.current_plugin = self.plugin_not_implemented

        self.current_plugin.start()

        self.reset_flashed_count()
        self.device_manager.ipcon.enumerate()

    def reset_flashed_count(self):
        self.spin_flashed_count.setValue(0)

    def increase_flashed_count(self):
        self.spin_flashed_count.setValue(self.spin_flashed_count.value() + 1)

    def flash_clicked(self):
        self.set_tool_status_normal('-')
        self.set_uid_status_normal('-')
        self.set_flash_status_normal('-')
        self.set_value_normal('-')

        if self.current_plugin != None:
            self.current_plugin.flash_clicked()

    def restart_test_clicked(self):
        # trigger test-restart by forcing an enumerate
        self.device_manager.ipcon.enumerate()

    def continue_clicked(self):
        if self.current_plugin != None:
            self.current_plugin.continue_clicked()

    def set_label_text(self, label, text, color):
        label.setText(text)

        if color != None:
            label.setStyleSheet('QLabel {{ color : {0} }}'.format(color))
        else:
            label.setStyleSheet('')

        QtWidgets.QApplication.processEvents()

    def set_tool_status_normal(self, text):
        self.set_label_text(self.label_tool_status, text, None)

    def set_tool_status_okay(self, text):
        self.set_label_text(self.label_tool_status, text, 'green')

    def set_tool_status_error(self, text):
        self.set_label_text(self.label_tool_status, text, 'red')

    def set_tool_status_action(self, text):
        self.set_label_text(self.label_tool_status, text, 'blue')

    def set_uid_status_normal(self, text):
        self.set_label_text(self.label_uid_status, text, None)

    def set_uid_status_okay(self, text):
        self.set_label_text(self.label_uid_status, text, 'green')

    def set_uid_status_error(self, text):
        self.set_label_text(self.label_uid_status, text, 'red')

    def set_uid_status_action(self, text):
        self.set_label_text(self.label_uid_status, text, 'blue')

    def set_flash_status_normal(self, text):
        self.set_label_text(self.label_flash_status, text, None)

    def set_flash_status_okay(self, text):
        self.set_label_text(self.label_flash_status, text, 'green')

    def set_flash_status_error(self, text):
        self.set_label_text(self.label_flash_status, text, 'red')

    def set_flash_status_action(self, text):
        self.set_label_text(self.label_flash_status, text, 'blue')

    def set_value_normal(self, text):
        self.set_label_text(self.label_value, text, None)

    def set_value_okay(self, text):
        self.set_label_text(self.label_value, text, 'green')

    def set_value_error(self, text):
        self.set_label_text(self.label_value, text, 'red')

    def set_value_action(self, text):
        self.set_label_text(self.label_value, text, 'blue')
