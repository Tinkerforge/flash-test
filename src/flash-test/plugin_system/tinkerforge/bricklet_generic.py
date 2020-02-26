# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2020-02-26.      #
#                                                           #
# Python Bindings Version 2.1.24                            #
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

GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletGeneric(Device):
    DEVICE_IDENTIFIER = -1
    DEVICE_DISPLAY_NAME = 'Generic'
    DEVICE_URL_PART = 'generic' # internal

    FUNCTION_GET_SPITFP_ERROR_COUNT = 234
    FUNCTION_SET_BOOTLOADER_MODE = 235
    FUNCTION_GET_BOOTLOADER_MODE = 236
    FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237
    FUNCTION_WRITE_FIRMWARE = 238
    FUNCTION_RESET = 243
    FUNCTION_WRITE_UID = 248
    FUNCTION_READ_UID = 249
    FUNCTION_GET_IDENTITY = 255

    BOOTLOADER_MODE_BOOTLOADER = 0
    BOOTLOADER_MODE_FIRMWARE = 1
    BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4
    BOOTLOADER_STATUS_OK = 0
    BOOTLOADER_STATUS_INVALID_MODE = 1
    BOOTLOADER_STATUS_NO_CHANGE = 2
    BOOTLOADER_STATUS_ENTRY_FUNCTION_NOT_PRESENT = 3
    BOOTLOADER_STATUS_DEVICE_IDENTIFIER_INCORRECT = 4
    BOOTLOADER_STATUS_CRC_MISMATCH = 5

    def __init__(self, uid, ipcon):
        Device.__init__(self, uid, ipcon, BrickletGeneric.DEVICE_IDENTIFIER, BrickletGeneric.DEVICE_DISPLAY_NAME)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletGeneric.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletGeneric.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGeneric.FUNCTION_SET_BOOTLOADER_MODE] = BrickletGeneric.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGeneric.FUNCTION_GET_BOOTLOADER_MODE] = BrickletGeneric.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGeneric.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletGeneric.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGeneric.FUNCTION_WRITE_FIRMWARE] = BrickletGeneric.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGeneric.FUNCTION_RESET] = BrickletGeneric.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGeneric.FUNCTION_WRITE_UID] = BrickletGeneric.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletGeneric.FUNCTION_READ_UID] = BrickletGeneric.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletGeneric.FUNCTION_GET_IDENTITY] = BrickletGeneric.RESPONSE_EXPECTED_ALWAYS_TRUE

        ipcon.add_device(self)

    def get_spitfp_error_count(self):
        #self.check_validity()

        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletGeneric.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

    def set_bootloader_mode(self, mode):
        #self.check_validity()

        mode = int(mode)

        return self.ipcon.send_request(self, BrickletGeneric.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        #self.check_validity()

        return self.ipcon.send_request(self, BrickletGeneric.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        #self.check_validity()

        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletGeneric.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        #self.check_validity()

        data = list(map(int, data))

        return self.ipcon.send_request(self, BrickletGeneric.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def reset(self):
        #self.check_validity()

        self.ipcon.send_request(self, BrickletGeneric.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        #self.check_validity()

        uid = int(uid)

        self.ipcon.send_request(self, BrickletGeneric.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        #self.check_validity()

        return self.ipcon.send_request(self, BrickletGeneric.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        return GetIdentity(*self.ipcon.send_request(self, BrickletGeneric.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

Generic = BrickletGeneric # for backward compatibility
