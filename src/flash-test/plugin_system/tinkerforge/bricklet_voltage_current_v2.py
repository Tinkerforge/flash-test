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

GetCurrentCallbackConfiguration = namedtuple('CurrentCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetVoltageCallbackConfiguration = namedtuple('VoltageCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetPowerCallbackConfiguration = namedtuple('PowerCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetConfiguration = namedtuple('Configuration', ['averaging', 'voltage_conversion_time', 'current_conversion_time'])
GetCalibration = namedtuple('Calibration', ['voltage_multiplier', 'voltage_divisor', 'current_multiplier', 'current_divisor'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletVoltageCurrentV2(Device):
    """
    Measures power, DC voltage and DC current up to 720W/36V/20A
    """

    DEVICE_IDENTIFIER = 2105
    DEVICE_DISPLAY_NAME = 'Voltage/Current Bricklet 2.0'
    DEVICE_URL_PART = 'voltage_current_v2' # internal

    CALLBACK_CURRENT = 4
    CALLBACK_VOLTAGE = 8
    CALLBACK_POWER = 12


    FUNCTION_GET_CURRENT = 1
    FUNCTION_SET_CURRENT_CALLBACK_CONFIGURATION = 2
    FUNCTION_GET_CURRENT_CALLBACK_CONFIGURATION = 3
    FUNCTION_GET_VOLTAGE = 5
    FUNCTION_SET_VOLTAGE_CALLBACK_CONFIGURATION = 6
    FUNCTION_GET_VOLTAGE_CALLBACK_CONFIGURATION = 7
    FUNCTION_GET_POWER = 9
    FUNCTION_SET_POWER_CALLBACK_CONFIGURATION = 10
    FUNCTION_GET_POWER_CALLBACK_CONFIGURATION = 11
    FUNCTION_SET_CONFIGURATION = 13
    FUNCTION_GET_CONFIGURATION = 14
    FUNCTION_SET_CALIBRATION = 15
    FUNCTION_GET_CALIBRATION = 16
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
    AVERAGING_1 = 0
    AVERAGING_4 = 1
    AVERAGING_16 = 2
    AVERAGING_64 = 3
    AVERAGING_128 = 4
    AVERAGING_256 = 5
    AVERAGING_512 = 6
    AVERAGING_1024 = 7
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

        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_CURRENT] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_CURRENT_CALLBACK_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_CURRENT_CALLBACK_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_VOLTAGE] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_VOLTAGE_CALLBACK_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_VOLTAGE_CALLBACK_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_POWER] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_POWER_CALLBACK_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_POWER_CALLBACK_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_CONFIGURATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_CALIBRATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_CALIBRATION] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_WRITE_FIRMWARE] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_RESET] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_WRITE_UID] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_READ_UID] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletVoltageCurrentV2.FUNCTION_GET_IDENTITY] = BrickletVoltageCurrentV2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletVoltageCurrentV2.CALLBACK_CURRENT] = 'i'
        self.callback_formats[BrickletVoltageCurrentV2.CALLBACK_VOLTAGE] = 'i'
        self.callback_formats[BrickletVoltageCurrentV2.CALLBACK_POWER] = 'i'


    def get_current(self):
        """
        Returns the current. The value is in mA
        and between -20000mA and 20000mA.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Current` callback. You can set the callback configuration
        with :func:`Set Current Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_CURRENT, (), '', 'i')

    def set_current_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Current` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Current` callback.

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

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_CURRENT_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c i i', '')

    def get_current_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Current Callback Configuration`.
        """
        return GetCurrentCallbackConfiguration(*self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_CURRENT_CALLBACK_CONFIGURATION, (), '', 'I ! c i i'))

    def get_voltage(self):
        """
        Returns the voltage. The value is in mV
        and between 0mV and 36000mV.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Voltage` callback. You can set the callback configuration
        with :func:`Set Voltage Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_VOLTAGE, (), '', 'i')

    def set_voltage_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Voltage` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Voltage` callback.

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

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_VOLTAGE_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c i i', '')

    def get_voltage_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Voltage Callback Configuration`.
        """
        return GetVoltageCallbackConfiguration(*self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_VOLTAGE_CALLBACK_CONFIGURATION, (), '', 'I ! c i i'))

    def get_power(self):
        """
        Returns the power. The value is in mW
        and between 0mV and 720000mW.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Power` callback. You can set the callback configuration
        with :func:`Set Power Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_POWER, (), '', 'i')

    def set_power_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Power` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Power` callback.

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

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_POWER_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c i i', '')

    def get_power_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Power Callback Configuration`.
        """
        return GetPowerCallbackConfiguration(*self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_POWER_CALLBACK_CONFIGURATION, (), '', 'I ! c i i'))

    def set_configuration(self, averaging, voltage_conversion_time, current_conversion_time):
        """
        Sets the configuration of the Voltage/Current Bricklet 2.0. It is
        possible to configure number of averages as well as
        voltage and current conversion time.

        Averaging:

        .. csv-table::
         :header: "Value", "Number of Averages"
         :widths: 20, 20

         "0",    "1"
         "1",    "4"
         "2",    "16"
         "3",    "64"
         "4",    "128"
         "5",    "256"
         "6",    "512"
         ">=7",  "1024"

        Voltage/Current conversion:

        .. csv-table::
         :header: "Value", "Conversion time"
         :widths: 20, 20

         "0",    "140µs"
         "1",    "204µs"
         "2",    "332µs"
         "3",    "588µs"
         "4",    "1.1ms"
         "5",    "2.116ms"
         "6",    "4.156ms"
         ">=7",  "8.244ms"

        The default values are 3, 4 and 4 (64, 1.1ms, 1.1ms) for averaging, voltage
        conversion and current conversion.
        """
        averaging = int(averaging)
        voltage_conversion_time = int(voltage_conversion_time)
        current_conversion_time = int(current_conversion_time)

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_CONFIGURATION, (averaging, voltage_conversion_time, current_conversion_time), 'B B B', '')

    def get_configuration(self):
        """
        Returns the configuration as set by :func:`Set Configuration`.
        """
        return GetConfiguration(*self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_CONFIGURATION, (), '', 'B B B'))

    def set_calibration(self, voltage_multiplier, voltage_divisor, current_multiplier, current_divisor):
        """
        Since the ADC and the shunt resistor used for the measurements
        are not perfect they need to be calibrated by a multiplier and
        a divisor if a very precise reading is needed.

        For example, if you are expecting a current of 1000mA and you
        are measuring 1023mA, you can calibrate the Voltage/Current Bricklet
        by setting the current multiplier to 1000 and the divisor to 1023.
        The same applies for the voltage.
        """
        voltage_multiplier = int(voltage_multiplier)
        voltage_divisor = int(voltage_divisor)
        current_multiplier = int(current_multiplier)
        current_divisor = int(current_divisor)

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_CALIBRATION, (voltage_multiplier, voltage_divisor, current_multiplier, current_divisor), 'H H H H', '')

    def get_calibration(self):
        """
        Returns the calibration as set by :func:`Set Calibration`.
        """
        return GetCalibration(*self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_CALIBRATION, (), '', 'H H H H'))

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
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

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

        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

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

        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletVoltageCurrentV2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

VoltageCurrentV2 = BrickletVoltageCurrentV2 # for backward compatibility
