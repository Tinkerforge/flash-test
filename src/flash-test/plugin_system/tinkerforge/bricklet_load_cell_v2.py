# -*- coding: utf-8 -*-
#############################################################
# This file was automatically generated on 2019-01-29.      #
#                                                           #
# Python Bindings Version 2.1.21                            #
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

GetWeightCallbackConfiguration = namedtuple('WeightCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetConfiguration = namedtuple('Configuration', ['rate', 'gain'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletLoadCellV2(Device):
    """
    Measures weight with a load cell
    """

    DEVICE_IDENTIFIER = 2104
    DEVICE_DISPLAY_NAME = 'Load Cell Bricklet 2.0'
    DEVICE_URL_PART = 'load_cell_v2' # internal

    CALLBACK_WEIGHT = 4


    FUNCTION_GET_WEIGHT = 1
    FUNCTION_SET_WEIGHT_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_WEIGHT_CALLBACK_CONFIGURATION = 3
    FUNCTION_SET_MOVING_AVERAGE = 5
    FUNCTION_GET_MOVING_AVERAGE = 6
    FUNCTION_SET_INFO_LED_CONFIG = 7
    FUNCTION_GET_INFO_LED_CONFIG = 8
    FUNCTION_CALIBRATE = 9
    FUNCTION_TARE = 10
    FUNCTION_SET_CONFIGURATION = 11
    FUNCTION_GET_CONFIGURATION = 12
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
    INFO_LED_CONFIG_OFF = 0
    INFO_LED_CONFIG_ON = 1
    INFO_LED_CONFIG_SHOW_HEARTBEAT = 2
    RATE_10HZ = 0
    RATE_80HZ = 1
    GAIN_128X = 0
    GAIN_64X = 1
    GAIN_32X = 2
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

        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_WEIGHT] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_SET_WEIGHT_CALLBACK_CONFIGURATION] = BrickletLoadCellV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_WEIGHT_CALLBACK_CONFIGURATION] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_SET_MOVING_AVERAGE] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_MOVING_AVERAGE] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_SET_INFO_LED_CONFIG] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_INFO_LED_CONFIG] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_CALIBRATE] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_TARE] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_SET_CONFIGURATION] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_CONFIGURATION] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_WRITE_FIRMWARE] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_RESET] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_WRITE_UID] = BrickletLoadCellV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletLoadCellV2.FUNCTION_READ_UID] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletLoadCellV2.FUNCTION_GET_IDENTITY] = BrickletLoadCellV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletLoadCellV2.CALLBACK_WEIGHT] = 'i'


    def get_weight(self):
        """
        Returns the currently measured weight in grams.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Weight` callback. You can set the callback configuration
        with :func:`Set Weight Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_WEIGHT, (), '', 'i')

    def set_weight_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Weight` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Weight` callback.

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

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_SET_WEIGHT_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c i i', '')

    def get_weight_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Weight Callback Configuration`.
        """
        return GetWeightCallbackConfiguration(*self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_WEIGHT_CALLBACK_CONFIGURATION, (), '', 'I ! c i i'))

    def set_moving_average(self, average):
        """
        Sets the length of a `moving averaging <https://en.wikipedia.org/wiki/Moving_average>`__
        for the weight value.

        Setting the length to 1 will turn the averaging off. With less
        averaging, there is more noise on the data.

        The range for the averaging is 1-100.

        The default value is 4.
        """
        average = int(average)

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_SET_MOVING_AVERAGE, (average,), 'H', '')

    def get_moving_average(self):
        """
        Returns the length moving average as set by :func:`Set Moving Average`.
        """
        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_MOVING_AVERAGE, (), '', 'H')

    def set_info_led_config(self, config):
        """
        Configures the info LED to be either turned off, turned on, or blink in
        heartbeat mode.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_SET_INFO_LED_CONFIG, (config,), 'B', '')

    def get_info_led_config(self):
        """
        Returns the LED configuration as set by :func:`Set Info LED Config`
        """
        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_INFO_LED_CONFIG, (), '', 'B')

    def calibrate(self, weight):
        """
        To calibrate your Load Cell Bricklet 2.0 you have to

        * empty the scale and call this function with 0 and
        * add a known weight to the scale and call this function with the weight in
          grams.

        The calibration is saved in the flash of the Bricklet and only
        needs to be done once.

        We recommend to use the Brick Viewer for calibration, you don't need
        to call this function in your source code.
        """
        weight = int(weight)

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_CALIBRATE, (weight,), 'I', '')

    def tare(self):
        """
        Sets the currently measured weight as tare weight.
        """
        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_TARE, (), '', '')

    def set_configuration(self, rate, gain):
        """
        The measurement rate and gain are configurable.

        The rate can be either 10Hz or 80Hz. A faster rate will produce more noise.
        It is additionally possible to add a moving average
        (see :func:`Set Moving Average`) to the measurements.

        The gain can be 128x, 64x or 32x. It represents a measurement range of
        ±20mV, ±40mV and ±80mV respectively. The Load Cell Bricklet uses an
        excitation voltage of 5V and most load cells use an output of 2mV/V. That
        means the voltage range is ±15mV for most load cells (i.e. gain of 128x
        is best). If you don't know what all of this means you should keep it at
        128x, it will most likely be correct.

        The default rate is 10Hz and the default gain is 128x.
        """
        rate = int(rate)
        gain = int(gain)

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_SET_CONFIGURATION, (rate, gain), 'B B', '')

    def get_configuration(self):
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        return GetConfiguration(*self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_CONFIGURATION, (), '', 'B B'))

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
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

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

        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

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

        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletLoadCellV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

LoadCellV2 = BrickletLoadCellV2 # for backward compatibility
