# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

bricklet_remote_switch.py: Remove Switch plugin

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

from ..tinkerforge.bricklet_remote_switch import BrickletRemoteSwitch
from ..plugin_base import PluginBase

class Plugin(PluginBase):
    TODO_TEXT = u"""\
1. Verbinde Remove Switch Bricklet mit Port C
2. Verbinde Test-Antenne mit Remove Switch Bricklet
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. Warte bis Wert sich auf "Alle Schaltbefehle wurden gesendet" ändert:
     * Die Funksteckdose muss währenddessen mehrfach klicken
6. Test-Antenne vom Bricklet abziehen
7. Das Bricklet ist fertig, mit Antenne in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""

    qtcb_switching_done = QtCore.pyqtSignal()

    def __init__(self, *args):
        PluginBase.__init__(self, *args)

        self.next_switch_to = BrickletRemoteSwitch.SWITCH_TO_OFF
        self.switchings_left = 5

        self.qtcb_switching_done.connect(self.cb_switching_done)

    def start(self, device_information):
        PluginBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletRemoteSwitch.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.write_new_uid_to_bricklet()
        self.write_plugin_to_bricklet(self.get_bricklets_firmware_directory('remote_switch'))
        self.master_reset()

    def new_enum(self, device_information):
        self.mw.set_tool_status_okay("Plugin gefunden")
        self.rs = BrickletRemoteSwitch(device_information.uid, self.get_ipcon())
        self.rs.register_callback(self.rs.CALLBACK_SWITCHING_DONE, self.qtcb_switching_done.emit)
        self.rs.switch_socket_a(11, 11, self.rs.SWITCH_TO_ON)
        self.next_switch_to = self.rs.SWITCH_TO_OFF
        self.switchings_left = 6
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
