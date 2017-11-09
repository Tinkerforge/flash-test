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

class BrickletXMCEMVTest(Device):
    """
    Bricklet for Infineon XMC EMV tests
    """

    DEVICE_IDENTIFIER = 280
    DEVICE_DISPLAY_NAME = 'XMC EMV Test Bricklet'

    CALLBACK_TEST = 2


    FUNCTION_GET_TEST = 1
    FUNCTION_GET_IDENTITY = 255


    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletXMCEMVTest.FUNCTION_GET_TEST] = BrickletXMCEMVTest.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletXMCEMVTest.FUNCTION_GET_IDENTITY] = BrickletXMCEMVTest.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletXMCEMVTest.CALLBACK_TEST] = '64B'


    def get_test(self, data_in):
        """

        """
        data_in = list(map(int, data_in))

        return self.ipcon.send_request(self, BrickletXMCEMVTest.FUNCTION_GET_TEST, (data_in,), '64B', '64B')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletXMCEMVTest.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

XMCEMVTest = BrickletXMCEMVTest # for backward compatibility
