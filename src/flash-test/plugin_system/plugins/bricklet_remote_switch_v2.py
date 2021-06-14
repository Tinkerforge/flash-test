# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_remote_switch_v2.py: Remote Switch 2.0 plugin

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

from ..tinkerforge.bricklet_remote_switch_v2 import BrickletRemoteSwitchV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Remote Switch Bricklet 2.0 mit Port D des Master Bricks 3.0
2. Verbinde Test-Antenne mit Remote Switch Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Warte bis Wert sich auf "Alle Schaltbefehle wurden gesendet" ändert:
     * Die Funksteckdose (Typ: A, House Code: [1,2,4], Receiver Code: [A,B,D]) muss währenddessen mehrfach klicken
6. Test-Antenne vom Bricklet abziehen
7. Das Bricklet ist fertig, mit Antenne in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    qtcb_switching_done = QtCore.pyqtSignal()

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)

        self.next_switch_to = BrickletRemoteSwitchV2.SWITCH_TO_OFF
        self.switchings_left = 5

        self.qtcb_switching_done.connect(self.cb_switching_done)

    def start(self):
        CoMCUBrickletBase.start(self)

    def get_device_identifier(self):
        return BrickletRemoteSwitchV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletRemoteSwitchV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        self.rs = BrickletRemoteSwitchV2(device_information.uid, self.get_ipcon())
        if self.rs.get_bootloader_mode() != BrickletRemoteSwitchV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.rs.register_callback(self.rs.CALLBACK_SWITCHING_DONE, self.qtcb_switching_done.emit)

        self.show_device_information(device_information)

        self.next_switch_to = self.rs.SWITCH_TO_OFF
        self.switchings_left = 2
        self.rs.switch_socket_a(11, 11, self.rs.SWITCH_TO_ON)

        self.mw.set_value_action("Einschaltbefehl wurde gesendet")

    def cb_switching_done(self):
        self.switchings_left -= 1

        if self.switchings_left > 0:
            if self.next_switch_to == self.rs.SWITCH_TO_OFF:
                self.rs.switch_socket_a(11, 11, self.rs.SWITCH_TO_OFF)
                self.mw.set_value_action("Ausschaltbefehl wurde gesendet")
                self.next_switch_to = self.rs.SWITCH_TO_ON
            else:
                self.rs.switch_socket_a(11, 11, self.rs.SWITCH_TO_ON)
                self.mw.set_value_action("Einschaltbefehl wurde gesendet")
                self.next_switch_to = self.rs.SWITCH_TO_OFF
        else:
            self.mw.set_value_normal("Alle Schaltbefehle wurden gesendet")
