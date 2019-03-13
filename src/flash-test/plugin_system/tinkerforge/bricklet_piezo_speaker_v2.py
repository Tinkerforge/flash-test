# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2018-11-27.      #
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

GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletPiezoSpeakerV2(Device):
    """

    """

    DEVICE_IDENTIFIER = 2145
    DEVICE_DISPLAY_NAME = 'Piezo Speaker Bricklet 2.0'
    DEVICE_URL_PART = 'piezo_speaker_v2' # internal

    CALLBACK_BEEP_FINISHED = 3
    CALLBACK_MORSE_CODE_FINISHED = 4


    FUNCTION_BEEP = 1
    FUNCTION_MORSE_CODE = 2
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

    BEEP_DURATION_OFF = 0
    BEEP_DURATION_INFINITE = 4294967295
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

        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_BEEP] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_MORSE_CODE] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_WRITE_FIRMWARE] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_RESET] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_WRITE_UID] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_READ_UID] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeakerV2.FUNCTION_GET_IDENTITY] = BrickletPiezoSpeakerV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletPiezoSpeakerV2.CALLBACK_BEEP_FINISHED] = ''
        self.callback_formats[BrickletPiezoSpeakerV2.CALLBACK_MORSE_CODE_FINISHED] = ''


    def beep(self, duration, frequency, volume):
        """
        Beeps with the given frequency for the duration in ms. For example:
        If you set a duration of 1000, with a frequency value of 2000
        the piezo buzzer will beep for one second with a frequency of
        approximately 2 kHz.

        A duration of 0 stops the current beep if any, the frequency parameter is
        ignored. A duration of 4294967295 results in an infinite beep.

        The *frequency* parameter can be set between 585 and 7100.
        """
        duration = int(duration)
        frequency = int(frequency)
        volume = int(volume)

        self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_BEEP, (duration, frequency, volume), 'I H B', '')

    def morse_code(self, morse, frequency, volume):
        """
        Sets morse code that will be played by the piezo buzzer. The morse code
        is given as a string consisting of "." (dot), "-" (minus) and " " (space)
        for *dits*, *dahs* and *pauses*. Every other character is ignored.
        The second parameter is the frequency (see :func:`Beep`).

        For example: If you set the string "...---...", the piezo buzzer will beep
        nine times with the durations "short short short long long long short
        short short".

        The maximum string size is 60.
        """
        morse = create_string(morse)
        frequency = int(frequency)
        volume = int(volume)

        self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_MORSE_CODE, (morse, frequency, volume), '60s H B', '')

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
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

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

        return self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

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

        return self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletPiezoSpeakerV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

PiezoSpeakerV2 = BrickletPiezoSpeakerV2 # for backward compatibility