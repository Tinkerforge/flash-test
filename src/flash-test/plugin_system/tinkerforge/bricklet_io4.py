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

GetConfiguration = namedtuple('Configuration', ['direction_mask', 'value_mask'])
GetMonoflop = namedtuple('Monoflop', ['value', 'time', 'time_remaining'])
GetEdgeCountConfig = namedtuple('EdgeCountConfig', ['edge_type', 'debounce'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletIO4(Device):
    """
    4-channel digital input/output
    """

    DEVICE_IDENTIFIER = 29
    DEVICE_DISPLAY_NAME = 'IO-4 Bricklet'

    CALLBACK_INTERRUPT = 9
    CALLBACK_MONOFLOP_DONE = 12

    FUNCTION_SET_VALUE = 1
    FUNCTION_GET_VALUE = 2
    FUNCTION_SET_CONFIGURATION = 3
    FUNCTION_GET_CONFIGURATION = 4
    FUNCTION_SET_DEBOUNCE_PERIOD = 5
    FUNCTION_GET_DEBOUNCE_PERIOD = 6
    FUNCTION_SET_INTERRUPT = 7
    FUNCTION_GET_INTERRUPT = 8
    FUNCTION_SET_MONOFLOP = 10
    FUNCTION_GET_MONOFLOP = 11
    FUNCTION_SET_SELECTED_VALUES = 13
    FUNCTION_GET_EDGE_COUNT = 14
    FUNCTION_SET_EDGE_COUNT_CONFIG = 15
    FUNCTION_GET_EDGE_COUNT_CONFIG = 16
    FUNCTION_GET_IDENTITY = 255

    DIRECTION_IN = 'i'
    DIRECTION_OUT = 'o'
    EDGE_TYPE_RISING = 0
    EDGE_TYPE_FALLING = 1
    EDGE_TYPE_BOTH = 2

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 1)

        self.response_expected[BrickletIO4.FUNCTION_SET_VALUE] = BrickletIO4.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIO4.FUNCTION_GET_VALUE] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIO4.FUNCTION_SET_CONFIGURATION] = BrickletIO4.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIO4.FUNCTION_GET_CONFIGURATION] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIO4.FUNCTION_SET_DEBOUNCE_PERIOD] = BrickletIO4.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletIO4.FUNCTION_GET_DEBOUNCE_PERIOD] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIO4.FUNCTION_SET_INTERRUPT] = BrickletIO4.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletIO4.FUNCTION_GET_INTERRUPT] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIO4.CALLBACK_INTERRUPT] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletIO4.FUNCTION_SET_MONOFLOP] = BrickletIO4.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIO4.FUNCTION_GET_MONOFLOP] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIO4.CALLBACK_MONOFLOP_DONE] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletIO4.FUNCTION_SET_SELECTED_VALUES] = BrickletIO4.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIO4.FUNCTION_GET_EDGE_COUNT] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIO4.FUNCTION_SET_EDGE_COUNT_CONFIG] = BrickletIO4.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletIO4.FUNCTION_GET_EDGE_COUNT_CONFIG] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletIO4.FUNCTION_GET_IDENTITY] = BrickletIO4.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletIO4.CALLBACK_INTERRUPT] = 'B B'
        self.callback_formats[BrickletIO4.CALLBACK_MONOFLOP_DONE] = 'B B'

    def set_value(self, value_mask):
        """
        Sets the output value (high or low) with a bitmask (4bit). A 1 in the bitmask
        means high and a 0 in the bitmask means low.
        
        For example: The value 3 or 0b0011 will turn the pins 0-1 high and the
        pins 2-3 low.
        
        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`SetConfiguration`.
        """
        self.ipcon.send_request(self, BrickletIO4.FUNCTION_SET_VALUE, (value_mask,), 'B', '')

    def get_value(self):
        """
        Returns a bitmask of the values that are currently measured.
        This function works if the pin is configured to input
        as well as if it is configured to output.
        """
        return self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_VALUE, (), '', 'B')

    def set_configuration(self, selection_mask, direction, value):
        """
        Configures the value and direction of the specified pins. Possible directions
        are 'i' and 'o' for input and output.
        
        If the direction is configured as output, the value is either high or low
        (set as *true* or *false*).
        
        If the direction is configured as input, the value is either pull-up or
        default (set as *true* or *false*).
        
        For example:
        
        * (15, 'i', true) or (0b1111, 'i', true) will set all pins of as input pull-up.
        * (8, 'i', false) or (0b1000, 'i', false) will set pin 3 of as input default (floating if nothing is connected).
        * (3, 'o', false) or (0b0011, 'o', false) will set pins 0 and 1 as output low.
        * (4, 'o', true) or (0b0100, 'o', true) will set pin 2 of as output high.
        
        The default configuration is input with pull-up.
        """
        self.ipcon.send_request(self, BrickletIO4.FUNCTION_SET_CONFIGURATION, (selection_mask, direction, value), 'B c ?', '')

    def get_configuration(self):
        """
        Returns a value bitmask and a direction bitmask. A 1 in the direction bitmask
        means input and a 0 in the bitmask means output.
        
        For example: A return value of (3, 5) or (0b0011, 0b0101) for direction and
        value means that:
        
        * pin 0 is configured as input pull-up,
        * pin 1 is configured as input default,
        * pin 2 is configured as output high and
        * pin 3 is are configured as output low.
        """
        return GetConfiguration(*self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_CONFIGURATION, (), '', 'B B'))

    def set_debounce_period(self, debounce):
        """
        Sets the debounce period of the :func:`Interrupt` callback in ms.
        
        For example: If you set this value to 100, you will get the interrupt
        maximal every 100ms. This is necessary if something that bounces is
        connected to the IO-4 Bricklet, such as a button.
        
        The default value is 100.
        """
        self.ipcon.send_request(self, BrickletIO4.FUNCTION_SET_DEBOUNCE_PERIOD, (debounce,), 'I', '')

    def get_debounce_period(self):
        """
        Returns the debounce period as set by :func:`SetDebouncePeriod`.
        """
        return self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_DEBOUNCE_PERIOD, (), '', 'I')

    def set_interrupt(self, interrupt_mask):
        """
        Sets the pins on which an interrupt is activated with a bitmask.
        Interrupts are triggered on changes of the voltage level of the pin,
        i.e. changes from high to low and low to high.
        
        For example: An interrupt bitmask of 10 or 0b1010 will enable the interrupt for
        pins 1 and 3.
        
        The interrupt is delivered with the callback :func:`Interrupt`.
        """
        self.ipcon.send_request(self, BrickletIO4.FUNCTION_SET_INTERRUPT, (interrupt_mask,), 'B', '')

    def get_interrupt(self):
        """
        Returns the interrupt bitmask as set by :func:`SetInterrupt`.
        """
        return self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_INTERRUPT, (), '', 'B')

    def set_monoflop(self, selection_mask, value_mask, time):
        """
        Configures a monoflop of the pins specified by the first parameter as 4 bit
        long bitmask. The specified pins must be configured for output. Non-output
        pins will be ignored.
        
        The second parameter is a bitmask with the desired value of the specified
        output pins. A 1 in the bitmask means high and a 0 in the bitmask means low.
        
        The third parameter indicates the time (in ms) that the pins should hold
        the value.
        
        If this function is called with the parameters (9, 1, 1500) or
        (0b1001, 0b0001, 1500): Pin 0 will get high and pin 3 will get low. In 1.5s pin
        0 will get low and pin 3 will get high again.
        
        A monoflop can be used as a fail-safe mechanism. For example: Lets assume you
        have a RS485 bus and an IO-4 Bricklet connected to one of the slave
        stacks. You can now call this function every second, with a time parameter
        of two seconds and pin 0 set to high. Pin 0 will be high all the time. If now
        the RS485 connection is lost, then pin 0 will get low in at most two seconds.
        """
        self.ipcon.send_request(self, BrickletIO4.FUNCTION_SET_MONOFLOP, (selection_mask, value_mask, time), 'B B I', '')

    def get_monoflop(self, pin):
        """
        Returns (for the given pin) the current value and the time as set by
        :func:`SetMonoflop` as well as the remaining time until the value flips.
        
        If the timer is not running currently, the remaining time will be returned
        as 0.
        """
        return GetMonoflop(*self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_MONOFLOP, (pin,), 'B', 'B I I'))

    def set_selected_values(self, selection_mask, value_mask):
        """
        Sets the output value (high or low) with a bitmask, according to
        the selection mask. The bitmask is 4 bit long, *true* refers to high 
        and *false* refers to low.
        
        For example: The parameters (9, 4) or (0b0110, 0b0100) will turn
        pin 1 low and pin 2 high, pin 0 and 3 will remain untouched.
        
        .. note::
         This function does nothing for pins that are configured as input.
         Pull-up resistors can be switched on with :func:`SetConfiguration`.
        """
        self.ipcon.send_request(self, BrickletIO4.FUNCTION_SET_SELECTED_VALUES, (selection_mask, value_mask), 'B B', '')

    def get_edge_count(self, pin, reset_counter):
        """
        Returns the current value of the edge counter for the selected pin. You can
        configure the edges that are counted with :func:`SetEdgeCountConfig`.
        
        If you set the reset counter to *true*, the count is set back to 0
        directly after it is read.
        
        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        return self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_EDGE_COUNT, (pin, reset_counter), 'B ?', 'I')

    def set_edge_count_config(self, selection_mask, edge_type, debounce):
        """
        Configures the edge counter for the selected pins.
        
        The edge type parameter configures if rising edges, falling edges or
        both are counted if the pin is configured for input. Possible edge types are:
        
        * 0 = rising (default)
        * 1 = falling
        * 2 = both
        
        The debounce time is given in ms.
        
        Configuring an edge counter resets its value to 0.
        
        If you don't know what any of this means, just leave it at default. The
        default configuration is very likely OK for you.
        
        Default values: 0 (edge type) and 100ms (debounce time)
        
        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        self.ipcon.send_request(self, BrickletIO4.FUNCTION_SET_EDGE_COUNT_CONFIG, (selection_mask, edge_type, debounce), 'B B B', '')

    def get_edge_count_config(self, pin):
        """
        Returns the edge type and debounce time for the selected pin as set by
        :func:`SetEdgeCountConfig`.
        
        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        return GetEdgeCountConfig(*self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_EDGE_COUNT_CONFIG, (pin,), 'B', 'B B'))

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletIO4.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

IO4 = BrickletIO4 # for backward compatibility
