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

from PyQt4 import QtCore

from plugin_system.tinkerforge.ip_connection import IPConnection
from plugin_system.tinkerforge.brick_master import BrickMaster
from plugin_system.tinkerforge.brick_master_flash_adapter_xmc import BrickMasterFlashAdapterXMC
from plugin_system.tinkerforge.bricklet_io4 import BrickletIO4
from plugin_system.tinkerforge.bricklet_industrial_quad_relay import BrickletIndustrialQuadRelay
from plugin_system.tinkerforge.bricklet_dmx import BrickletDMX
from collections import namedtuple

DeviceInformation = namedtuple('DeviceInformation', 'uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type')

class DeviceManager(QtCore.QObject):
    HOST = "localhost"
    PORT = 4223

    devices = {}
    flash_adapter_xmc_uid = None
    qtcb_enumerate = QtCore.pyqtSignal(str, str, str, type((0,)), type((0,)), int, int)

    def __init__(self, mw):
        QtCore.QObject.__init__(self)

        self.mw = mw

        self.qtcb_enumerate.connect(self.cb_enumerate)

        self.ipcon = IPConnection()
        self.ipcon.connect(self.HOST, self.PORT)
        self.ipcon.register_callback(self.ipcon.CALLBACK_ENUMERATE, self.qtcb_enumerate.emit)
        self.ipcon.enumerate()

    def cb_enumerate(self, uid, connected_uid, position, hardware_version, 
                     firmware_version, device_identifier, enumeration_type):
        if enumeration_type in (self.ipcon.ENUMERATION_TYPE_CONNECTED, self.ipcon.ENUMERATION_TYPE_AVAILABLE):
            if device_identifier == BrickletIO4.DEVICE_IDENTIFIER and uid == '555555':
                if self.mw.foot_pedal != None:
                    self.mw.foot_pedal.register_callback(BrickletIO4.CALLBACK_INTERRUPT, None)
                else:
                    self.mw.foot_pedal = BrickletIO4(uid, self.ipcon)
                    self.mw.foot_pedal.register_callback(BrickletIO4.CALLBACK_INTERRUPT, self.mw.qtcb_foot_pedal.emit)
                    self.mw.foot_pedal.set_interrupt(1)

                return
            
            # Flash Adapter XMC quad relay and control master
            if (device_identifier == BrickletIndustrialQuadRelay.DEVICE_IDENTIFIER and uid == '555') or \
               (device_identifier == BrickMaster.DEVICE_IDENTIFIER and uid in ('6qZ5ow', '6R62QC', '5VjDHm', '6DdLE5')):
                return
            
            # Flash Adapter XMC program masster
            if device_identifier == BrickMasterFlashAdapterXMC.DEVICE_IDENTIFIER and uid in ('6qzRzc', '6kP6n3', '6Jprbj', '6DdMSG'):
                # Override old UID if new Flash adapter is connected
                # We don't support two flash adapter simultaneously
                self.flash_adapter_xmc_uid = uid
                return
                
            # DMX Master
            if device_identifier == BrickletDMX.DEVICE_IDENTIFIER and uid == 'dmxT1':
                return

            device_information = DeviceInformation(uid, connected_uid, position, hardware_version,
                                                   firmware_version, device_identifier, enumeration_type)

            # Overwrite device if it already exists
            self.devices[device_identifier] = device_information
            if self.mw.current_plugin:
                if (self.mw.current_plugin.get_device_identifier() % 10000) == device_identifier:
                    self.mw.current_plugin.new_enum(device_information)
                    return

            if device_identifier == BrickMaster.DEVICE_IDENTIFIER and \
               self.mw.label_tool_status.text() == 'Master Brick startet neu':
                self.mw.set_tool_status_normal('Master Brick wurde neu gestartet')
