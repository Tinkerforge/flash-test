# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

brick_master.py: Master plugin

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

from ..tinkerforge.brick_master import BrickMaster
from ..extension_base import ExtensionBase
from ..callback_emulator import CallbackEmulator

class Plugin(ExtensionBase):
    TODO_TEXT = u"""\
1. Stecker RS485 Extension auf Master Brick
2. Verbinde RS485 Stapel miteinander
3. Verbinde Master Brick mit PC per Mini-USB
4. Falls Brick nicht geflasht wird, drücke "Erase"- und "Reset"-Taster
5. Überprüfe Wert 
6. Gehe zu 1 
"""
    def start(self, device_information):
        ExtensionBase.start(self, device_information)

    def get_device_identifier(self):
        return 10000 + BrickMaster.DEVICE_IDENTIFIER
    
    def reconfigure(self, master):
        master.set_extension_type(0, 2)
        master.set_rs485_configuration(1000000, 'n', 1)
        master.set_rs485_address(0)
        master.set_rs485_slave_address(0, 42)
        master.set_rs485_slave_address(1, 0)
        typ = master.get_extension_type(0)
        conf = master.get_rs485_configuration()
        adr = master.get_rs485_address()
        slave_adr = (master.get_rs485_slave_address(0), master.get_rs485_slave_address(1))
        if conf == (1000000, 'n', 1) and adr == 0 and typ == 2 and slave_adr == (42, 0):
            self.mw.set_value_action('RS485 Extension konfiguriert')
            master.reset()
        else:
            self.mw.set_value_error('Konnte Extension nicht konfigurieren')

    def new_enum(self, device_information):
        master = BrickMaster(device_information.uid, self.get_ipcon())
        if master.is_rs485_present():
            typ = master.get_extension_type(0)
            conf = master.get_rs485_configuration()
            adr = master.get_rs485_address()
            slave_adr = (master.get_rs485_slave_address(0), master.get_rs485_slave_address(1))
            if conf == (1000000, 'n', 1) and adr == 0 and typ == 2 and slave_adr == (42, 0):
                self.mw.set_value_action('RS485 Master gefunden. Drücke Reset-Knopf an RS485 Slave.')
            elif conf == (1000000, 'n', 1) and adr == 42 and typ == 2 and slave_adr == (0, 0):
                self.mw.set_value_okay('RS485 Slave gefunden. Alles OK!')
            else:
                self.reconfigure(master)
                
        else:
            self.reconfigure(master)

