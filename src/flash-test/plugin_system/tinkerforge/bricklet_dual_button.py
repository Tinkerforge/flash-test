# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2016-09-08.      #
#                                                           #
# Python Bindings Version 2.1.10                            #
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

GetLEDState = namedtuple('LEDState', ['led_l', 'led_r'])
GetButtonState = namedtuple('ButtonState', ['button_l', 'button_r'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletDualButton(Device):
    """
    Two tactile buttons with built-in blue LEDs
    """

    DEVICE_IDENTIFIER = 230
    DEVICE_DISPLAY_NAME = 'Dual Button Bricklet'

    CALLBACK_STATE_CHANGED = 4

    FUNCTION_SET_LED_STATE = 1
    FUNCTION_GET_LED_STATE = 2
    FUNCTION_GET_BUTTON_STATE = 3
    FUNCTION_SET_SELECTED_LED_STATE = 5
    FUNCTION_GET_IDENTITY = 255

    LED_STATE_AUTO_TOGGLE_ON = 0
    LED_STATE_AUTO_TOGGLE_OFF = 1
    LED_STATE_ON = 2
    LED_STATE_OFF = 3
    BUTTON_STATE_PRESSED = 0
    BUTTON_STATE_RELEASED = 1
    LED_LEFT = 0
    LED_RIGHT = 1

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 0)

        self.response_expected[BrickletDualButton.FUNCTION_SET_LED_STATE] = BrickletDualButton.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletDualButton.FUNCTION_GET_LED_STATE] = BrickletDualButton.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletDualButton.FUNCTION_GET_BUTTON_STATE] = BrickletDualButton.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletDualButton.CALLBACK_STATE_CHANGED] = BrickletDualButton.RESPONSE_EXPECTED_ALWAYS_FALSE
        self.response_expected[BrickletDualButton.FUNCTION_SET_SELECTED_LED_STATE] = BrickletDualButton.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletDualButton.FUNCTION_GET_IDENTITY] = BrickletDualButton.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletDualButton.CALLBACK_STATE_CHANGED] = 'B B B B'

    def set_led_state(self, led_l, led_r):
        """
        Sets the state of the LEDs. Possible states are:
        
        * 0 = AutoToggleOn: Enables auto toggle with initially enabled LED.
        * 1 = AutoToggleOff: Activates auto toggle with initially disabled LED.
        * 2 = On: Enables LED (auto toggle is disabled).
        * 3 = Off: Disables LED (auto toggle is disabled).
        
        In auto toggle mode the LED is toggled automatically at each press of a button.
        
        If you just want to set one of the LEDs and don't know the current state
        of the other LED, you can get the state with :func:`GetLEDState` or you
        can use :func:`SetSelectedLEDState`.
        
        The default value is (1, 1).
        """
        self.ipcon.send_request(self, BrickletDualButton.FUNCTION_SET_LED_STATE, (led_l, led_r), 'B B', '')

    def get_led_state(self):
        """
        Returns the current state of the LEDs, as set by :func:`SetLEDState`.
        """
        return GetLEDState(*self.ipcon.send_request(self, BrickletDualButton.FUNCTION_GET_LED_STATE, (), '', 'B B'))

    def get_button_state(self):
        """
        Returns the current state for both buttons. Possible states are:
        
        * 0 = pressed
        * 1 = released
        """
        return GetButtonState(*self.ipcon.send_request(self, BrickletDualButton.FUNCTION_GET_BUTTON_STATE, (), '', 'B B'))

    def set_selected_led_state(self, led, state):
        """
        Sets the state of the selected LED (0 or 1). 
        
        The other LED remains untouched.
        """
        self.ipcon.send_request(self, BrickletDualButton.FUNCTION_SET_SELECTED_LED_STATE, (led, state), 'B B', '')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to, 
        the position, the hardware and firmware version as well as the
        device identifier.
        
        The position can be 'a', 'b', 'c' or 'd'.
        
        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletDualButton.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, id, callback):
        """
        Registers a callback with ID *id* to the function *callback*.
        """
        self.registered_callbacks[id] = callback

DualButton = BrickletDualButton # for backward compatibility
