# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2019-08-23.      #
#                                                           #
# Python Bindings Version 2.1.23                            #
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

GetColor = namedtuple('Color', ['r', 'g', 'b', 'c'])
GetColorCallbackConfiguration = namedtuple('ColorCallbackConfiguration', ['period', 'value_has_to_change'])
GetIlluminanceCallbackConfiguration = namedtuple('IlluminanceCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetColorTemperatureCallbackConfiguration = namedtuple('ColorTemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetConfiguration = namedtuple('Configuration', ['gain', 'integration_time'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletColorV2(Device):
    """
    Measures color (RGB value), illuminance and color temperature
    """

    DEVICE_IDENTIFIER = 2128
    DEVICE_DISPLAY_NAME = 'Color Bricklet 2.0'
    DEVICE_URL_PART = 'color_v2' # internal

    CALLBACK_COLOR = 4
    CALLBACK_ILLUMINANCE = 8
    CALLBACK_COLOR_TEMPERATURE = 12


    FUNCTION_GET_COLOR = 1
    FUNCTION_SET_COLOR_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_COLOR_CALLBACK_CONFIGURATION = 3
    FUNCTION_GET_ILLUMINANCE = 5
    FUNCTION_SET_ILLUMINANCE_CALLBACK_CONFIGURATION = 6
    FUNCTION_GET_ILLUMINANCE_CALLBACK_CONFIGURATION = 7
    FUNCTION_GET_COLOR_TEMPERATURE = 9
    FUNCTION_SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION = 10
    FUNCTION_GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION = 11
    FUNCTION_SET_LIGHT = 13
    FUNCTION_GET_LIGHT = 14
    FUNCTION_SET_CONFIGURATION = 15
    FUNCTION_GET_CONFIGURATION = 16
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

    THRESHOLD_OPTION_OFF = 'x'
    THRESHOLD_OPTION_OUTSIDE = 'o'
    THRESHOLD_OPTION_INSIDE = 'i'
    THRESHOLD_OPTION_SMALLER = '<'
    THRESHOLD_OPTION_GREATER = '>'
    GAIN_1X = 0
    GAIN_4X = 1
    GAIN_16X = 2
    GAIN_60X = 3
    INTEGRATION_TIME_2MS = 0
    INTEGRATION_TIME_24MS = 1
    INTEGRATION_TIME_101MS = 2
    INTEGRATION_TIME_154MS = 3
    INTEGRATION_TIME_700MS = 4
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

        self.response_expected[BrickletColorV2.FUNCTION_GET_COLOR] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_COLOR_CALLBACK_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_COLOR_CALLBACK_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_ILLUMINANCE] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_ILLUMINANCE_CALLBACK_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_ILLUMINANCE_CALLBACK_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_COLOR_TEMPERATURE] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_LIGHT] = BrickletColorV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletColorV2.FUNCTION_GET_LIGHT] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletColorV2.FUNCTION_GET_CONFIGURATION] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletColorV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletColorV2.FUNCTION_WRITE_FIRMWARE] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletColorV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletColorV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_RESET] = BrickletColorV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletColorV2.FUNCTION_WRITE_UID] = BrickletColorV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletColorV2.FUNCTION_READ_UID] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletColorV2.FUNCTION_GET_IDENTITY] = BrickletColorV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletColorV2.CALLBACK_COLOR] = 'H H H H'
        self.callback_formats[BrickletColorV2.CALLBACK_ILLUMINANCE] = 'I'
        self.callback_formats[BrickletColorV2.CALLBACK_COLOR_TEMPERATURE] = 'H'


    def get_color(self):
        """
        Returns the measured color of the sensor. The values
        have a range of 0 to 65535.

        The red (r), green (g), blue (b) and clear (c) colors are measured
        with four different photodiodes that are responsive at different
        wavelengths:

        .. image:: /Images/Bricklets/bricklet_color_wavelength_chart_600.jpg
           :scale: 100 %
           :alt: Chart Responsivity / Wavelength
           :align: center
           :target: ../../_images/Bricklets/bricklet_color_wavelength_chart_600.jpg

        If you want to get the color periodically, it is recommended
        to use the :cb:`Color` callback and set the period with
        :func:`Set Color Callback Configuration`.
        """
        return GetColor(*self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_COLOR, (), '', 'H H H H'))

    def set_color_callback_configuration(self, period, value_has_to_change):
        """
        The period in ms is the period with which the :cb:`Color`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change within the
        period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        The default value is (0, false).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_COLOR_CALLBACK_CONFIGURATION, (period, value_has_to_change), 'I !', '')

    def get_color_callback_configuration(self):
        """
        Returns the callback configuration as set by
        :func:`Set Color Callback Configuration`.
        """
        return GetColorCallbackConfiguration(*self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_COLOR_CALLBACK_CONFIGURATION, (), '', 'I !'))

    def get_illuminance(self):
        """
        Returns the illuminance affected by the gain and integration time as
        set by :func:`Set Configuration`. To get the illuminance in Lux apply this formula::

         lux = illuminance * 700 / gain / integration_time

        To get a correct illuminance measurement make sure that the color
        values themselves are not saturated. The color value (R, G or B)
        is saturated if it is equal to the maximum value of 65535.
        In that case you have to reduce the gain, see :func:`Set Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Illuminance` callback. You can set the callback configuration
        with :func:`Set Illuminance Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_ILLUMINANCE, (), '', 'I')

    def set_illuminance_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Illuminance` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Illuminance` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_ILLUMINANCE_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c I I', '')

    def get_illuminance_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Illuminance Callback Configuration`.
        """
        return GetIlluminanceCallbackConfiguration(*self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_ILLUMINANCE_CALLBACK_CONFIGURATION, (), '', 'I ! c I I'))

    def get_color_temperature(self):
        """
        Returns the color temperature in Kelvin.

        To get a correct color temperature measurement make sure that the color
        values themselves are not saturated. The color value (R, G or B)
        is saturated if it is equal to the maximum value of 65535.
        In that case you have to reduce the gain, see :func:`Set Configuration`.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Color Temperature` callback. You can set the callback configuration
        with :func:`Set Color Temperature Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_COLOR_TEMPERATURE, (), '', 'H')

    def set_color_temperature_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Color Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Color Temperature` callback.

        The following options are possible:

        .. csv-table::
         :header: "Option", "Description"
         :widths: 10, 100

         "'x'",    "Threshold is turned off"
         "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
         "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
         "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
         "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

        If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.

        The default value is (0, false, 'x', 0, 0).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)
        option = create_char(option)
        min = int(min)
        max = int(max)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c H H', '')

    def get_color_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Color Temperature Callback Configuration`.
        """
        return GetColorTemperatureCallbackConfiguration(*self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_COLOR_TEMPERATURE_CALLBACK_CONFIGURATION, (), '', 'I ! c H H'))

    def set_light(self, enable):
        """
        Turns the white LED on the Bricklet on/off.
        """
        enable = bool(enable)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_LIGHT, (enable,), '!', '')

    def get_light(self):
        """
        Returns the value as set by :func:`Set Light`.
        """
        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_LIGHT, (), '', '!')

    def set_configuration(self, gain, integration_time):
        """
        Sets the configuration of the sensor. Gain and integration time
        can be configured this way.

        For configuring the gain:

        * 0: 1x Gain
        * 1: 4x Gain
        * 2: 16x Gain
        * 3: 60x Gain

        For configuring the integration time:

        * 0: 2.4ms
        * 1: 24ms
        * 2: 101ms
        * 3: 154ms
        * 4: 700ms

        Increasing the gain enables the sensor to detect a
        color from a higher distance.

        The integration time provides a trade-off between conversion time
        and accuracy. With a longer integration time the values read will
        be more accurate but it will take longer to get the conversion
        results.

        The default values are 60x gain and 154ms integration time.
        """
        gain = int(gain)
        integration_time = int(integration_time)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_CONFIGURATION, (gain, integration_time), 'B B', '')

    def get_configuration(self):
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        return GetConfiguration(*self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_CONFIGURATION, (), '', 'B B'))

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
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

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

        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

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

        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletColorV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletColorV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletColorV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

ColorV2 = BrickletColorV2 # for backward compatibility
