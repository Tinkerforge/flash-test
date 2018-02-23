# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2018-02-23.      #
#                                                           #
# Python Bindings Version 2.1.15                            #
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

class BrickletPiezoSpeaker(Device):
    """
    Creates beep with configurable frequency
    """

    DEVICE_IDENTIFIER = 242
    DEVICE_DISPLAY_NAME = 'Piezo Speaker Bricklet'
    DEVICE_URL_PART = 'piezo_speaker' # internal

    CALLBACK_BEEP_FINISHED = 4
    CALLBACK_MORSE_CODE_FINISHED = 5


    FUNCTION_BEEP = 1
    FUNCTION_MORSE_CODE = 2
    FUNCTION_CALIBRATE = 3
    FUNCTION_GET_IDENTITY = 255

    BEEP_DURATION_OFF = 0
    BEEP_DURATION_INFINITE = 4294967295

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletPiezoSpeaker.FUNCTION_BEEP] = BrickletPiezoSpeaker.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeaker.FUNCTION_MORSE_CODE] = BrickletPiezoSpeaker.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletPiezoSpeaker.FUNCTION_CALIBRATE] = BrickletPiezoSpeaker.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletPiezoSpeaker.FUNCTION_GET_IDENTITY] = BrickletPiezoSpeaker.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletPiezoSpeaker.CALLBACK_BEEP_FINISHED] = ''
        self.callback_formats[BrickletPiezoSpeaker.CALLBACK_MORSE_CODE_FINISHED] = ''


    def beep(self, duration, frequency):
        """
        Beeps with the given frequency for the duration in ms. For example:
        If you set a duration of 1000, with a frequency value of 2000
        the piezo buzzer will beep for one second with a frequency of
        approximately 2 kHz.

        .. versionchanged:: 2.0.2$nbsp;(Plugin)
           A duration of 0 stops the current beep if any, the frequency parameter is
           ignored. A duration of 4294967295 results in an infinite beep.

        The *frequency* parameter can be set between 585 and 7100.

        The Piezo Speaker Bricklet can only approximate the frequency, it will play
        the best possible match by applying the calibration (see :func:`Calibrate`).
        """
        duration = int(duration)
        frequency = int(frequency)

        self.ipcon.send_request(self, BrickletPiezoSpeaker.FUNCTION_BEEP, (duration, frequency), 'I H', '')

    def morse_code(self, morse, frequency):
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

        self.ipcon.send_request(self, BrickletPiezoSpeaker.FUNCTION_MORSE_CODE, (morse, frequency), '60s H', '')

    def calibrate(self):
        """
        The Piezo Speaker Bricklet can play 512 different tones. This function
        plays each tone and measures the exact frequency back. The result is a
        mapping between setting value and frequency. This mapping is stored
        in the EEPROM and loaded on startup.

        The Bricklet should come calibrated, you only need to call this
        function (once) every time you reflash the Bricklet plugin.

        Returns *true* after the calibration finishes.
        """
        return self.ipcon.send_request(self, BrickletPiezoSpeaker.FUNCTION_CALIBRATE, (), '', '!')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletPiezoSpeaker.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

PiezoSpeaker = BrickletPiezoSpeaker # for backward compatibility
