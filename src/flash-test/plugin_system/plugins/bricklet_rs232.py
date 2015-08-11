# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

bricklet_rs232.py: RS232 plugin

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

from ..tinkerforge.bricklet_rs232 import BrickletRS232
from ..plugin_base import PluginBase

from ..callback_emulator import CallbackEmulator

class Plugin(PluginBase):
    TODO_TEXT = u"""\
1. Verbinde RS232 Bricklet mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
4. Warte bis Wert sich auf "Test OK!" ändert
5. Das Bricklet ist fertig. In ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben.
6. Gehe zu 1
"""

    def __init__(self, *args):
        self.message = ''
        PluginBase.__init__(self, *args)

    def start(self, device_information):
        PluginBase.start(self, device_information)
        
        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletRS232.DEVICE_IDENTIFIER
    
    def flash_clicked(self):
        self.write_new_uid_to_bricklet()
        self.write_plugin_to_bricklet(self.get_bricklets_firmware_directory('rs232'))
        self.master_reset()
        
    def new_enum(self, device_information):
        def string_to_char_list(message):
            chars = list(message)
            chars.extend(['\0']*(60 - len(message)))
            return chars, len(message)
        
        def char_list_to_string(message, length):
            return ''.join(message[:length])
        
        def cb_read(message, length):
            s = char_list_to_string(message, length)
            self.message += s
            if self.message == '0123456789'*6:
                self.message = ''
                self.mw.label_value.setText("Test OK!")
                
        if device_information:
            self.mw.label_tool_status.setText("Plugin gefunden")
            self.mw.label_value.setText("Warte auf Antwort")
            self.rs232 = BrickletRS232(device_information.uid, self.get_ipcon())
            self.rs232.register_callback(self.rs232.CALLBACK_READ_CALLBACK, cb_read)
            self.rs232.enable_read_callback()

            self.rs232.write(*string_to_char_list('0123456789'*6))
            