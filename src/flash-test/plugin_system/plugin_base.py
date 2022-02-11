# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015-2017 Olaf Lüke <olaf@tinkerforge.com>

ft.py: Base for plugins

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
from PyQt5.QtWidgets import QMessageBox
from .tinkerforge.brick_master import BrickMaster
from .tinkerforge.ip_connection import IPConnection

import urllib.request
import urllib.parse
import traceback
import os

BASE58 = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
def base58encode(value):
    encoded = ''
    while value >= 58:
        div, mod = divmod(value, 58)
        encoded = BASE58[mod] + encoded
        value = div
    encoded = BASE58[value] + encoded
    return encoded

class PluginBase(QtWidgets.QWidget, object):
    TODO_TEXT = 'Dieses Plugin ist noch nicht implementiert.'

    def __init__(self, mw):
        QtWidgets.QWidget.__init__(self)

        self.mw = mw
        self.device_information = None

    def get_new_uid(self):
        return int(urllib.request.urlopen('https://stagingwww.tinkerforge.com/uid', timeout=15).read())

    def get_ipcon(self):
        return self.mw.device_manager.ipcon

    def get_master_uid(self):
        return self.mw.get_master_brick_device_information().uid

    def get_current_master(self):
        master_uid = self.get_master_uid()
        master = BrickMaster(master_uid, self.get_ipcon())
        return master

    def master_reset(self):
        try:
            self.get_current_master().reset()
        except:
            traceback.print_exc()
            self.mw.set_tool_status_error('Konnte Master Brick nicht neustarten')
            QMessageBox.critical(self.mw, "Konnte Master Brick nicht neustarten.", "Konnte Master Brick nicht neustarten:\nTraceback ist im Terminal.")
        else:
            self.mw.set_tool_status_action('Master Brick startet neu')

    def flash_bricklet(self, plugin_filename):
        plugin_success = self.write_plugin_to_bricklet(plugin_filename)
        uid_success = self.write_new_uid_to_bricklet()

        if uid_success and plugin_success:
            self.master_reset()

    # To be overridden by bricklet class
    def write_new_uid_to_bricklet(self):
        print("write_new_uid_to_bricklet not Implemented")
        return False

    def write_plugin_to_bricklet(self, plugin_filename):
        print("write_new_uid_to_bricklet not Implemented")
        return False

    # To be overridden by inheriting class
    def stop(self):
        pass

    def start(self):
        self.mw.button_continue.hide()
        self.mw.text_edit_todo.setPlainText(self.TODO_TEXT)

    def new_enum(self, device_information):
        pass

    def is_comcu(self):
        return False

    def destroy(self):
        pass

    def get_device_identifier(self):
        return -1

    def flash_clicked(self):
        pass

    def continue_clicked(self):
        pass
