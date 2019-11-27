# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2019-11-27.      #
#                                                           #
# Python Bindings Version 2.1.24                            #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

#### __DEVICE_IS_NOT_RELEASED__ ####

from collections import namedtuple

try:
    from .ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data
except ValueError:
    from ip_connection import Device, IPConnection, Error, create_char, create_char_list, create_string, create_chunk_data

GetValue = namedtuple('Value', ['timestamp', 'value'])

class TNGDI8(Device):
    """
    TBD
    """

    DEVICE_IDENTIFIER = 201
    DEVICE_DISPLAY_NAME = 'TNG DI8'
    DEVICE_URL_PART = 'di8' # internal



    FUNCTION_GET_VALUE = 1
    FUNCTION_GET_TIMESTAMP = 234
    FUNCTION_COPY_FIRMWARE = 235
    FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237
    FUNCTION_WRITE_FIRMWARE = 238
    FUNCTION_RESET = 243

    COPY_STATUS_OK = 0
    COPY_STATUS_DEVICE_IDENTIFIER_INCORRECT = 1
    COPY_STATUS_MAGIC_NUMBER_INCORRECT = 2
    COPY_STATUS_LENGTH_MALFORMED = 3
    COPY_STATUS_CRC_MISMATCH = 4

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[TNGDI8.FUNCTION_GET_VALUE] = TNGDI8.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[TNGDI8.FUNCTION_GET_TIMESTAMP] = TNGDI8.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[TNGDI8.FUNCTION_COPY_FIRMWARE] = TNGDI8.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[TNGDI8.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = TNGDI8.RESPONSE_EXPECTED_FALSE
        self.response_expected[TNGDI8.FUNCTION_WRITE_FIRMWARE] = TNGDI8.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[TNGDI8.FUNCTION_RESET] = TNGDI8.RESPONSE_EXPECTED_FALSE



    def get_value(self):
        """
        Returns the input value as bools, *true* refers to high and *false* refers to low.
        """
        return GetValue(*self.ipcon.send_request(self, TNGDI8.FUNCTION_GET_VALUE, (), '', 'Q 8!'))

    def get_timestamp(self):
        """
        TODO
        """
        return self.ipcon.send_request(self, TNGDI8.FUNCTION_GET_TIMESTAMP, (), '', 'Q')

    def copy_firmware(self):
        """
        TODO
        """
        return self.ipcon.send_request(self, TNGDI8.FUNCTION_COPY_FIRMWARE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        TODO
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, TNGDI8.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        """
        TODO
        """
        data = list(map(int, data))

        return self.ipcon.send_request(self, TNGDI8.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def reset(self):
        """
        Calling this function will reset the TNG module. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, TNGDI8.FUNCTION_RESET, (), '', '')
