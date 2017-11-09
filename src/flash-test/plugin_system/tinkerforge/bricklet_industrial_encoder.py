# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2017-11-09.      #
#                                                           #
# Python Bindings Version 2.1.14                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data

GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletIndustrialEncoder(Device):
    """
    TODO
    """

    DEVICE_IDENTIFIER = 281
    DEVICE_DISPLAY_NAME = 'Industrial Encoder Bricklet'



    FUNCTION_GET_IDENTITY = 255


    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletIndustrialEncoder.FUNCTION_GET_IDENTITY] = BrickletIndustrialEncoder.RESPONSE_EXPECTED_ALWAYS_TRUE



    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletIndustrialEncoder.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

IndustrialEncoder = BrickletIndustrialEncoder # for backward compatibility
