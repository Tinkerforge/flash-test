# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

extension_rs485.py: RS485 Extension plugin

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

class Plugin(ExtensionBase):
    TODO_TEXT = u"""\
Vorbereitung: RS485 Slave mit Adresse 42, Speed 1000000, Parity None und Stopbits 1 konfigurieren und über USB Netzteil versorgen

1. Verbinde RS485 Stapel miteinander
2. Stecker RS485 Extension auf Master Brick
3. Starte RS485 Master neu
4. Warte bis RS485 Master gefunden wird
5. Starter RS485 Slave neu
6. Warte bis RS485 Slave gefunden wird
7. Die Extension ist fertig, mit grauem 3-Pol Stecker in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""
    def start(self, device_information):
        ExtensionBase.start(self, device_information)

    def stop(self):
        ExtensionBase.stop(self)

    def get_device_identifier(self):
        return BrickMaster.EXTENSION_TYPE_RS485*10000 + BrickMaster.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        master = BrickMaster(device_information.uid, self.get_ipcon())

        if master.is_ethernet_present(): # slave
            self.mw.set_value_okay('RS485 Slave gefunden. Alles OK!')
            return

        if not master.is_rs485_present():
            self.mw.set_value_action('RS485 Extension Typ gesetzt')
            master.set_extension_type(0, BrickMaster.EXTENSION_TYPE_RS485)
            master.reset()
            return

        master.set_rs485_configuration(1000000, 'n', 1)
        master.set_rs485_address(0)
        master.set_rs485_slave_address(0, 42)
        master.set_rs485_slave_address(1, 0)
        typ = master.get_extension_type(0)
        conf = master.get_rs485_configuration()
        adr = master.get_rs485_address()
        slave_adr = (master.get_rs485_slave_address(0), master.get_rs485_slave_address(1))
        if conf == (1000000, 'n', 1) and adr == 0 and typ == 2 and slave_adr == (42, 0):
            self.mw.set_value_action('RS485 Extension konfiguriert, drücke Reset-Knopf an RS485 Slave')
            master.reset()
        else:
            self.mw.set_value_error('Konnte RS485 Extension nicht konfigurieren')

