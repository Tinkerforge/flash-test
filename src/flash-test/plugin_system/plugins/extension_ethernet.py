# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

extension_ethernet.py: Ethernet Extension plugin

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

from ..tinkerforge.brick_master import BrickMaster
from ..extension_base import ExtensionBase

import time

class Plugin(ExtensionBase):
    TODO_TEXT = u"""\
1. Verbinde Ethernet-Kabel mit Ethernet Extension (über PoE falls möglich)
2. Stecke Ethernet Extension auf Master Brick
3. Starte Master Brick neu
4. Warte bis Ethernet gefunden wird
5. Trage MAC Adresse ein und drücke Knopf "Mac Adresse schreiben"
6. Warte bis Ethernet-Verbindung hergestellt wird
7. Falls mit PoE: Entferne USB. Läuft Master weiter?
8. MAC Adressen-Aufkleber aufkleben
9. Die Extension ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
10. Gehe zu 1
"""
    def start(self):
        self.device_information = None
        self.master = None

        self.mw.edit_ethernet_extension.setInputMask("H:HH;_")
        self.mw.edit_ethernet_extension.setText("0:01")
        self.mw.button_ethernet_extension.clicked.connect(self.button_clicked)
        ExtensionBase.start(self)

    def stop(self):
        super().stop()
        self.mw.button_ethernet_extension.clicked.disconnect(self.button_clicked)
        self.mw.hide_layout(self.mw.ethernet_extension_layout)
        ExtensionBase.stop(self)

    def get_device_identifier(self):
        return BrickMaster.EXTENSION_TYPE_ETHERNET*10000 + BrickMaster.DEVICE_IDENTIFIER

    def try_connect(self):
        i = 0
        range_to = 200
        for i in range(range_to):
            status = self.master.get_ethernet_status()
            if status.ip != (0, 0, 0, 0):
                i = 0
                break
            time.sleep(0.1)

        if i == range_to-1:
            self.mw.set_value_error('Konnte keine Ethernet-Verbindung aufbauen')
            return


        self.mw.set_value_okay('Ethernet-Verbindung aufgebaut. Fertig!')

    def button_clicked(self):
        if self.master == None or self.device_information == None:
            self.mw.set_value_error('self.master == None or self.device_information == None')
            return

        mac_prefix = "40:D8:55:02:A"
        mac_str = mac_prefix + str(self.mw.edit_ethernet_extension.text())
        if len(mac_str) != 12 + 5:
            self.mw.set_value_error('MAC Adresse hat ungültige Länge')
            return

        mac = mac_str.split(':')
        if len(mac) != 6:
            self.mw.set_value_error('MAC Adresse hat ungültige Länge')
            return

        mac = [int(x, 16) for x in mac]

        self.master.set_ethernet_mac_address(mac)
        self.master.set_ethernet_hostname('Tinkerforge' + ''.join(['%02X' % x for x in mac[3:]]))
        self.master.reset()
        self.mw.set_value_action('Übertrage MAC Adresse')

        mac[-1] += 1
        if mac[-1] > 255:
            mac[-1] = 0
            mac[-2] += 1

        self.mw.edit_ethernet_extension.setText(':'.join(['%02X' % x for x in mac])[-4:])

    def new_enum(self, device_information):
        self.device_information = device_information
        self.master = BrickMaster(device_information.uid, self.get_ipcon())
        if self.master.is_ethernet_present():
            self.mw.show_layout(self.mw.ethernet_extension_layout)
            status = self.master.get_ethernet_status()
            if status.mac_address[4] == 0xA0 and status.mac_address[5] == 0x00:
                self.mw.set_value_action('MAC Adresse eintragen und auf "Mac Adresse Schreiben" klicken')
            else:
                mac = map(hex, status.mac_address)
                mac = map(lambda x: x.replace('0x', ''), mac)
                mac = map(lambda x: '0'+x if len(x) == 1 else x, mac)
                self.mw.set_value_action('Versuche Ethernet-Verbindung aufzubauen (Mac: ' + ':'.join(mac).upper() + ')')
                QtCore.QTimer.singleShot(0.1, self.try_connect)
        else:
            self.master.set_extension_type(0, BrickMaster.EXTENSION_TYPE_ETHERNET)
            self.master.reset()
            self.mw.set_value_action('Extension-Typ geschrieben, starte Master neu')
