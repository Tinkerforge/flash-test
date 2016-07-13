# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2016-06-30.      #
#                                                           #
# Python Bindings Version 2.1.9                             #
#                                                           #
# If you have a bugfix for this file and want to commit it, #
# please fix the bug in the generator. You can find a link  #
# to the generators git repository on tinkerforge.com       #
#############################################################

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

GetCountCallbackThreshold = namedtuple('CountCallbackThreshold', ['option', 'min', 'max'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletRotaryEncoder(Device):
    """
    360° rotary encoder with push-button
    """

    DEVICE_IDENTIFIER = 236
    DEVICE_DISPLAY_NAME = 'Rotary Encoder Bricklet'

    CALLBACK_COUNT = 8
    CALLBACK_COUNT_REACHED = 9
    CALLBACK_PRESSED = 11
    CALLBACK_RELEASED = 12

    FUNCTION_GET_COUNT = 1
    FUNCTION_SET_COUNT_CALLBACK_PERIOD = 2
    FUNCTION_GET_COUNT_CALLBACK_PERIOD = 3
    FUNCTION_SET_COUNT_CALLBACK_THRESHOLD = 4
    FUNCTION_GET_COUNT_CALLBACK_THRESHOLD = 5
    FUNCTION_SET_DEBOUNCE_PERIOD = 6
    FUNCTION_GET_DEBOUNCE_PERIOD = 7
    FUNCTION_IS_PRESSED = 10
    FUNCTION_GET_IDENTITY = 255

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletRotaryEncoder.FUNCTION_GET_COUNT] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_SET_COUNT_CALLBACK_PERIOD] = BrickletRotaryEncoder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_GET_COUNT_CALLBACK_PERIOD] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_SET_COUNT_CALLBACK_THRESHOLD] = BrickletRotaryEncoder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_GET_COUNT_CALLBACK_THRESHOLD] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_SET_DEBOUNCE_PERIOD] = BrickletRotaryEncoder.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_GET_DEBOUNCE_PERIOD] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRotaryEncoder.CALLBACK_COUNT] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRotaryEncoder.CALLBACK_COUNT_REACHED] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_IS_PRESSED] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRotaryEncoder.CALLBACK_PRESSED] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRotaryEncoder.CALLBACK_RELEASED] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletRotaryEncoder.FUNCTION_GET_IDENTITY] = BrickletRotaryEncoder.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletRotaryEncoder.CALLBACK_COUNT] = 'i'
        self.callback_formats[BrickletRotaryEncoder.CALLBACK_COUNT_REACHED] = 'i'
        self.callback_formats[BrickletRotaryEncoder.CALLBACK_PRESSED] = ''
        self.callback_formats[BrickletRotaryEncoder.CALLBACK_RELEASED] = ''

    def get_count(self, reset):
        """
        Returns the current count of the encoder. If you set reset
        to true, the count is set back to 0 directly after the
        current count is read.
        
        The encoder has 24 steps per rotation
        
        Turning the encoder to the left decrements the counter,
        so a negative count is possible.
        """
        return self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_GET_COUNT, (reset,), '?', 'i')

    def set_count_callback_period(self, period):
        """
        Sets the period in ms with which the :func:`Count` callback is triggered
        periodically. A value of 0 turns the callback off.
        
        :func:`Count` is only triggered if the count has changed since the
        last triggering.
        
        The default value is 0.
        """
        self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_SET_COUNT_CALLBACK_PERIOD, (period,), 'I', '')

    def get_count_callback_period(self):
        """
        Returns the period as set by :func:`SetCountCallbackPeriod`.
        """
        return self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_GET_COUNT_CALLBACK_PERIOD, (), '', 'I')

    def set_count_callback_threshold(self, option, min, max):
        """
        Sets the thresholds for the :func:`CountReached` callback. 
        
        The following options are possible:
        
        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100
        
         "'x'",    "Callback is turned off"
         "'o'",    "Callback is triggered when the count is *outside* the min and max values"
         "'i'",    "Callback is triggered when the count is *inside* the min and max values"
         "'<'",    "Callback is triggered when the count is smaller than the min value (max is ignored)"
         "'>'",    "Callback is triggered when the count is greater than the min value (max is ignored)"
        
        The default value is ('x', 0, 0).
        """
        self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_SET_COUNT_CALLBACK_THRESHOLD, (option, min, max), 'c i i', '')

    def get_count_callback_threshold(self):
        """
        Returns the threshold as set by :func:`SetCountCallbackThreshold`.
        """
        return GetCountCallbackThreshold(*self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_GET_COUNT_CALLBACK_THRESHOLD, (), '', 'c i i'))

    def set_debounce_period(self, debounce):
        """
        Sets the period in ms with which the threshold callback
        
        * :func:`CountReached`
        
        is triggered, if the thresholds
        
        * :func:`SetCountCallbackThreshold`
        
        keeps being reached.
        
        The default value is 100.
        """
        self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_SET_DEBOUNCE_PERIOD, (debounce,), 'I', '')

    def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`SetDebouncePeriod`.
        """
        return self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_GET_DEBOUNCE_PERIOD, (), '', 'I')

    def is_pressed(self):
        """
        Returns *true* if the button is pressed and *false* otherwise.
        
        It is recommended to use the :func:`Pressed` and :func:`Released` callbacks
        to handle the button.
        """
        return self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_IS_PRESSED, (), '', '?')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletRotaryEncoder.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

RotaryEncoder = BrickletRotaryEncoder # for backward compatibility
