# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

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

from PyQt4 import Qt, QtGui, QtCore
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

class PluginBase(QtGui.QWidget, object):
    TODO_TEXT = 'Dieses Plugin ist noch nicht implementiert.'
    
    def __init__(self, mw):
        QtGui.QWidget.__init__(self)
        
        self.mw = mw
        self.device_information = None
        
    def get_new_uid(self):
        return int(urllib.request.urlopen('http://stagingwww.tinkerforge.com/uid').read())
        
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
        else:
            self.mw.set_tool_status_action('Master Brick startet neu')

    def write_new_uid_to_bricklet(self):
        try:
            uid = base58encode(int(self.get_new_uid()))
        except:
            traceback.print_exc()
            self.mw.set_uid_status_error('Konnte keine neue UID von tinkerforge.com abfragen')
            return False

        try:
            port = 'c'
            self.get_ipcon().write_bricklet_uid(self.get_current_master(), port, uid)
            uid_read = self.get_ipcon().read_bricklet_uid(self.get_current_master(), port)
            if uid != uid_read:
                self.mw.set_uid_status_error("Konnte UID an Port " + port.upper() + ' nicht verifizieren')
                return False
        except:
            traceback.print_exc()
            self.mw.set_uid_status_error('Konnte UID für Port ' + port.upper() + ' nicht setzen')
            return False

        self.mw.set_uid_status_okay('Neue UID "' + uid + '" für Port ' + port.upper() + ' gesetzt')
        return True

    def write_plugin_to_bricklet(self, plugin_filename):
        try:
            port = 'c'
            plugin = open(plugin_filename, mode='rb').read()
            plugin_chunks = []
            offset = 0
            ipcon = self.get_ipcon()
            master = self.get_current_master()
    
            while offset < len(plugin):
                chunk = plugin[offset:offset + IPConnection.PLUGIN_CHUNK_SIZE]
    
                if len(chunk) < IPConnection.PLUGIN_CHUNK_SIZE:
                    chunk += b'\0' * (IPConnection.PLUGIN_CHUNK_SIZE - len(chunk))
    
                chunk = list(chunk)
    
                plugin_chunks.append(chunk)
                offset += IPConnection.PLUGIN_CHUNK_SIZE
    
            position = 0
            for chunk in plugin_chunks:
                ipcon.write_bricklet_plugin(master, port, position, chunk)

                position += 1

                self.mw.set_flash_status_action("Schreibe Port " + port.upper() +  ": " + str(position) + '/' + str(len(plugin_chunks)))
                
            position = 0
            for chunk in plugin_chunks:
                self.mw.set_flash_status_action("Verifiziere Port " + port.upper() + ": " + str(position) + '/' + str(len(plugin_chunks)))
                read_chunk = list((ipcon.read_bricklet_plugin(master, port, position)))

                if read_chunk != chunk:
                    self.mw.set_flash_status_error("Konnte Plugin an Port " + port.upper() + ' nicht verifizieren')
                    return False
                position += 1
        except:
            traceback.print_exc()
            return False
        else:
            self.mw.set_flash_status_okay("Plugin auf Port " + port.upper() + ' geschrieben und verifiziert')
            
        return True

    def flash_bricklet(self, plugin_filename):
        uid_success = self.write_new_uid_to_bricklet()
        plugin_success = self.write_plugin_to_bricklet(plugin_filename)

        if uid_success and plugin_success:
            self.master_reset()

    # To be overridden by inheriting class
    def stop(self):
        pass
    
    def start(self, device_information):
        self.mw.button_continue.hide()
        self.device_information = device_information
        self.mw.text_edit_todo.setPlainText(self.TODO_TEXT)
            
    def new_enum(self, device_information):
        pass

    def destroy(self):
        pass
    
    def get_device_identifier(self):
        return -1
    
    def flash_clicked(self):
        pass

    def continue_clicked(self):
        pass
