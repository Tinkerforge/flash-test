# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

device_manager.py: Store UIDs of new Bricks/Bricklets etc

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

from plugin_system.tinkerforge.ip_connection import IPConnection
from collections import namedtuple

DeviceInformation = namedtuple('DeviceInformation', 'uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type')

class DeviceManager:
    HOST = "localhost"
    PORT = 4223

    devices = {}
    def __init__(self, mw):
        self.mw = mw
        self.ipcon = IPConnection()
        self.ipcon.connect(DeviceManager.HOST, DeviceManager.PORT)

        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, self.cb_enumerate)
        self.ipcon.enumerate()
    
    def cb_enumerate(self, uid, connected_uid, position, hardware_version, 
                     firmware_version, device_identifier, enumeration_type):
        if enumeration_type in (IPConnection.ENUMERATION_TYPE_CONNECTED, IPConnection.ENUMERATION_TYPE_AVAILABLE):
            device_information = DeviceInformation(uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type)

            # Overwrite device if it already exists
            self.devices[device_identifier] = device_information
            if self.mw.current_plugin:
                if self.mw.current_plugin.get_device_identifier() == device_identifier:
                    self.mw.current_plugin.new_enum(device_information)
