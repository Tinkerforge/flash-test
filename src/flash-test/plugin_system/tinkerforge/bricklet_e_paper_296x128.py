# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2019-01-28.      #
#                                                           #
# Python Bindings Version 2.1.20                            #
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

ReadBlackWhiteLowLevel = namedtuple('ReadBlackWhiteLowLevel', ['pixels_length', 'pixels_chunk_offset', 'pixels_chunk_data'])
ReadRedLowLevel = namedtuple('ReadRedLowLevel', ['pixels_length', 'pixels_chunk_offset', 'pixels_chunk_data'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletEPaper296x128(Device):
    """
    TBD
    """

    DEVICE_IDENTIFIER = 2146
    DEVICE_DISPLAY_NAME = 'E-Paper 296x128 Bricklet'
    DEVICE_URL_PART = 'e_paper_296x128' # internal



    FUNCTION_DRAW = 1
    FUNCTION_WRITE_BLACK_WHITE_LOW_LEVEL = 2
    FUNCTION_READ_BLACK_WHITE_LOW_LEVEL = 3
    FUNCTION_WRITE_RED_LOW_LEVEL = 4
    FUNCTION_READ_RED_LOW_LEVEL = 5
    FUNCTION_CLEAR_DISPLAY = 6
    FUNCTION_GET_SPITFP_ERROR_COUNT = 234
    FUNCTION_SET_BOOTLOADER_MODE = 235
    FUNCTION_GET_BOOTLOADER_MODE = 236
    FUNCTION_SET_WRITE_FIRMWARE_POINTER = 237
    FUNCTION_WRITE_FIRMWARE = 238
    FUNCTION_SET_STATUS_LED_CONFIG = 239
    FUNCTION_GET_STATUS_LED_CONFIG = 240
    FUNCTION_GET_CHIP_TEMPERATURE = 242
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
    STATUS_LED_CONFIG_OFF = 0
    STATUS_LED_CONFIG_ON = 1
    STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2
    STATUS_LED_CONFIG_SHOW_STATUS = 3

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletEPaper296x128.FUNCTION_DRAW] = BrickletEPaper296x128.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletEPaper296x128.FUNCTION_WRITE_BLACK_WHITE_LOW_LEVEL] = BrickletEPaper296x128.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_READ_BLACK_WHITE_LOW_LEVEL] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_WRITE_RED_LOW_LEVEL] = BrickletEPaper296x128.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_READ_RED_LOW_LEVEL] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_CLEAR_DISPLAY] = BrickletEPaper296x128.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletEPaper296x128.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_SET_BOOTLOADER_MODE] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_GET_BOOTLOADER_MODE] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletEPaper296x128.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletEPaper296x128.FUNCTION_WRITE_FIRMWARE] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletEPaper296x128.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletEPaper296x128.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_RESET] = BrickletEPaper296x128.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletEPaper296x128.FUNCTION_WRITE_UID] = BrickletEPaper296x128.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletEPaper296x128.FUNCTION_READ_UID] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletEPaper296x128.FUNCTION_GET_IDENTITY] = BrickletEPaper296x128.RESPONSE_EXPECTED_ALWAYS_TRUE



    def draw(self, draw_black_white, draw_red, x_start, y_start, x_end, y_end):
        """
        buffer -> display
        """
        draw_black_white = bool(draw_black_white)
        draw_red = bool(draw_red)
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)

        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_DRAW, (draw_black_white, draw_red, x_start, y_start, x_end, y_end), '! ! H B H B', '')

    def write_black_white_low_level(self, x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)
        pixels_length = int(pixels_length)
        pixels_chunk_offset = int(pixels_chunk_offset)
        pixels_chunk_data = list(map(bool, pixels_chunk_data))

        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_WRITE_BLACK_WHITE_LOW_LEVEL, (x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data), 'H B H B H H 432!', '')

    def read_black_white_low_level(self, x_start, y_start, x_end, y_end):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)

        return ReadBlackWhiteLowLevel(*self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_READ_BLACK_WHITE_LOW_LEVEL, (x_start, y_start, x_end, y_end), 'H B H B', 'H H 464!'))

    def write_red_low_level(self, x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)
        pixels_length = int(pixels_length)
        pixels_chunk_offset = int(pixels_chunk_offset)
        pixels_chunk_data = list(map(bool, pixels_chunk_data))

        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_WRITE_RED_LOW_LEVEL, (x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data), 'H B H B H H 432!', '')

    def read_red_low_level(self, x_start, y_start, x_end, y_end):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)

        return ReadRedLowLevel(*self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_READ_RED_LOW_LEVEL, (x_start, y_start, x_end, y_end), 'H B H B', 'H H 464!'))

    def clear_display(self):
        """
        Clears the complete content of the display.
        """
        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_CLEAR_DISPLAY, (), '', '')

    def get_spitfp_error_count(self):
        """
        Returns the error count for the communication between Brick and Bricklet.

        The errors are divided into

        * ACK checksum errors,
        * message checksum errors,
        * framing errors and
        * overflow errors.

        The errors counts are for errors that occur on the Bricklet side. All
        Bricks have a similar function that returns the errors on the Brick side.
        """
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

    def set_bootloader_mode(self, mode):
        """
        Sets the bootloader mode and returns the status after the requested
        mode change was instigated.

        You can change from bootloader mode to firmware mode and vice versa. A change
        from bootloader mode to firmware mode will only take place if the entry function,
        device identifier and CRC are present and correct.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        mode = int(mode)

        return self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

    def write_firmware(self, data):
        """
        Writes 64 Bytes of firmware at the position as written by
        :func:`Set Write Firmware Pointer` before. The firmware is written
        to flash every 4 chunks.

        You can only write firmware in bootloader mode.

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        data = list(map(int, data))

        return self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletEPaper296x128.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def write_black_white(self, x_start, y_start, x_end, y_end, pixels):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)
        pixels = list(map(bool, pixels))

        if len(pixels) > 65535:
            raise Error(Error.INVALID_PARAMETER, 'Pixels can be at most 65535 items long')

        pixels_length = len(pixels)
        pixels_chunk_offset = 0

        if pixels_length == 0:
            pixels_chunk_data = [False] * 432
            ret = self.write_black_white_low_level(x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data)
        else:
            with self.stream_lock:
                while pixels_chunk_offset < pixels_length:
                    pixels_chunk_data = create_chunk_data(pixels, pixels_chunk_offset, 432, False)
                    ret = self.write_black_white_low_level(x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data)
                    pixels_chunk_offset += 432

        return ret

    def read_black_white(self, x_start, y_start, x_end, y_end):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)

        with self.stream_lock:
            ret = self.read_black_white_low_level(x_start, y_start, x_end, y_end)
            pixels_length = ret.pixels_length
            pixels_out_of_sync = ret.pixels_chunk_offset != 0
            pixels_data = ret.pixels_chunk_data

            while not pixels_out_of_sync and len(pixels_data) < pixels_length:
                ret = self.read_black_white_low_level(x_start, y_start, x_end, y_end)
                pixels_length = ret.pixels_length
                pixels_out_of_sync = ret.pixels_chunk_offset != len(pixels_data)
                pixels_data += ret.pixels_chunk_data

            if pixels_out_of_sync: # discard remaining stream to bring it back in-sync
                while ret.pixels_chunk_offset + 464 < pixels_length:
                    ret = self.read_black_white_low_level(x_start, y_start, x_end, y_end)
                    pixels_length = ret.pixels_length

                raise Error(Error.STREAM_OUT_OF_SYNC, 'Pixels stream is out-of-sync')

        return pixels_data[:pixels_length]

    def write_red(self, x_start, y_start, x_end, y_end, pixels):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)
        pixels = list(map(bool, pixels))

        if len(pixels) > 65535:
            raise Error(Error.INVALID_PARAMETER, 'Pixels can be at most 65535 items long')

        pixels_length = len(pixels)
        pixels_chunk_offset = 0

        if pixels_length == 0:
            pixels_chunk_data = [False] * 432
            ret = self.write_red_low_level(x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data)
        else:
            with self.stream_lock:
                while pixels_chunk_offset < pixels_length:
                    pixels_chunk_data = create_chunk_data(pixels, pixels_chunk_offset, 432, False)
                    ret = self.write_red_low_level(x_start, y_start, x_end, y_end, pixels_length, pixels_chunk_offset, pixels_chunk_data)
                    pixels_chunk_offset += 432

        return ret

    def read_red(self, x_start, y_start, x_end, y_end):
        """

        """
        x_start = int(x_start)
        y_start = int(y_start)
        x_end = int(x_end)
        y_end = int(y_end)

        with self.stream_lock:
            ret = self.read_red_low_level(x_start, y_start, x_end, y_end)
            pixels_length = ret.pixels_length
            pixels_out_of_sync = ret.pixels_chunk_offset != 0
            pixels_data = ret.pixels_chunk_data

            while not pixels_out_of_sync and len(pixels_data) < pixels_length:
                ret = self.read_red_low_level(x_start, y_start, x_end, y_end)
                pixels_length = ret.pixels_length
                pixels_out_of_sync = ret.pixels_chunk_offset != len(pixels_data)
                pixels_data += ret.pixels_chunk_data

            if pixels_out_of_sync: # discard remaining stream to bring it back in-sync
                while ret.pixels_chunk_offset + 464 < pixels_length:
                    ret = self.read_red_low_level(x_start, y_start, x_end, y_end)
                    pixels_length = ret.pixels_length

                raise Error(Error.STREAM_OUT_OF_SYNC, 'Pixels stream is out-of-sync')

        return pixels_data[:pixels_length]

EPaper296x128 = BrickletEPaper296x128 # for backward compatibility
