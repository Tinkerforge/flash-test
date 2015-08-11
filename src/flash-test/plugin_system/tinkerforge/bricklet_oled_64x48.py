# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2015-06-23.      #
#                                                           #
# Bindings Version 2.1.4                                    #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

#### __DEVICE_IS_NOT_RELEASED__ ####

try:
    from collections import namedtuple
except ImportError:
    try:
        from .ip_connection import namedtuple
    except ValueError:
        from ip_connection import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error
except ValueError:
    from ip_connection import Device, IPConnection, Error

GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletOLED64x48(Device):
    """
    0.66" OLED with 64x48 pixels
    """

    DEVICE_IDENTIFIER = 264
    DEVICE_DISPLAY_NAME = 'OLED 64x48 Bricklet'


    FUNCTION_WRITE = 1
    FUNCTION_NEW_WINDOW = 2
    FUNCTION_CLEAR_DISPLAY = 3
    FUNCTION_DISPLAY_ON = 4
    FUNCTION_DISPLAY_OFF = 5
    FUNCTION_IS_DISPLAY_ON = 6
    FUNCTION_GET_IDENTITY = 255


    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletOLED64x48.FUNCTION_WRITE] = BrickletOLED64x48.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED64x48.FUNCTION_NEW_WINDOW] = BrickletOLED64x48.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED64x48.FUNCTION_CLEAR_DISPLAY] = BrickletOLED64x48.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED64x48.FUNCTION_DISPLAY_ON] = BrickletOLED64x48.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED64x48.FUNCTION_DISPLAY_OFF] = BrickletOLED64x48.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletOLED64x48.FUNCTION_IS_DISPLAY_ON] = BrickletOLED64x48.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletOLED64x48.FUNCTION_GET_IDENTITY] = BrickletOLED64x48.RESPONSE_EXPECTED_ALWAYS_TRUE


    def write(self, data):
        """
        
        """
        self.ipcon.send_request(self, BrickletOLED64x48.FUNCTION_WRITE, (data,), '64B', '')

    def new_window(self, column_from, column_to, row_from, row_to):
        """
        
        """
        self.ipcon.send_request(self, BrickletOLED64x48.FUNCTION_NEW_WINDOW, (column_from, column_to, row_from, row_to), 'B B B B', '')

    def clear_display(self):
        """
        
        """
        self.ipcon.send_request(self, BrickletOLED64x48.FUNCTION_CLEAR_DISPLAY, (), '', '')

    def display_on(self):
        """
        
        """
        self.ipcon.send_request(self, BrickletOLED64x48.FUNCTION_DISPLAY_ON, (), '', '')

    def display_off(self):
        """
        
        """
        self.ipcon.send_request(self, BrickletOLED64x48.FUNCTION_DISPLAY_OFF, (), '', '')

    def is_display_on(self):
        """
        
        """
        return self.ipcon.send_request(self, BrickletOLED64x48.FUNCTION_IS_DISPLAY_ON, (), '', '?')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletOLED64x48.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

OLED64x48 = BrickletOLED64x48 # for backward compatibility
