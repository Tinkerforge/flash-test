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

GetAllValues = namedtuple('AllValues', ['co2_concentration', 'temperature', 'humidity'])
GetAllValuesCallbackConfiguration = namedtuple('AllValuesCallbackConfiguration', ['period', 'value_has_to_change'])
GetCO2ConcentrationCallbackConfiguration = namedtuple('CO2ConcentrationCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetTemperatureCallbackConfiguration = namedtuple('TemperatureCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetHumidityCallbackConfiguration = namedtuple('HumidityCallbackConfiguration', ['period', 'value_has_to_change', 'option', 'min', 'max'])
GetSPITFPErrorCount = namedtuple('SPITFPErrorCount', ['error_count_ack_checksum', 'error_count_message_checksum', 'error_count_frame', 'error_count_overflow'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletCO2V2(Device):
    """
    Measures CO2 concentration, temperature and humidity
    """

    DEVICE_IDENTIFIER = 2147
    DEVICE_DISPLAY_NAME = 'CO2 Bricklet 2.0'
    DEVICE_URL_PART = 'co2_v2' # internal

    CALLBACK_ALL_VALUES = 8
    CALLBACK_CO2_CONCENTRATION = 12
    CALLBACK_TEMPERATURE = 16
    CALLBACK_HUMIDITY = 20


    FUNCTION_GET_ALL_VALUES = 1
    FUNCTION_SET_AIR_PRESSURE = 2
    FUNCTION_GET_AIR_PRESSURE = 3
    FUNCTION_SET_TEMPERATURE_OFFSET = 4
    FUNCTION_GET_TEMPERATURE_OFFSET = 5
    FUNCTION_SET_ALL_VALUES_CALLBACK_CONFIGURATION = 6
    FUNCTION_GET_ALL_VALUES_CALLBACK_CONFIGURATION = 7
    FUNCTION_GET_CO2_CONCENTRATION = 9
    FUNCTION_SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION = 10
    FUNCTION_GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION = 11
    FUNCTION_GET_TEMPERATURE = 13
    FUNCTION_SET_TEMPERATURE_CALLBACK_CONFIGURATION = 14
    FUNCTION_GET_TEMPERATURE_CALLBACK_CONFIGURATION = 15
    FUNCTION_GET_HUMIDITY = 17
    FUNCTION_SET_HUMIDITY_CALLBACK_CONFIGURATION = 18
    FUNCTION_GET_HUMIDITY_CALLBACK_CONFIGURATION = 19
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

        self.response_expected[BrickletCO2V2.FUNCTION_GET_ALL_VALUES] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_AIR_PRESSURE] = BrickletCO2V2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_AIR_PRESSURE] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_TEMPERATURE_OFFSET] = BrickletCO2V2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_TEMPERATURE_OFFSET] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_ALL_VALUES_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_ALL_VALUES_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_CO2_CONCENTRATION] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_TEMPERATURE] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_TEMPERATURE_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_HUMIDITY] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_HUMIDITY_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_HUMIDITY_CALLBACK_CONFIGURATION] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_SPITFP_ERROR_COUNT] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_BOOTLOADER_MODE] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_BOOTLOADER_MODE] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_WRITE_FIRMWARE_POINTER] = BrickletCO2V2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletCO2V2.FUNCTION_WRITE_FIRMWARE] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_SET_STATUS_LED_CONFIG] = BrickletCO2V2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_STATUS_LED_CONFIG] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_CHIP_TEMPERATURE] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_RESET] = BrickletCO2V2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletCO2V2.FUNCTION_WRITE_UID] = BrickletCO2V2.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletCO2V2.FUNCTION_READ_UID] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletCO2V2.FUNCTION_GET_IDENTITY] = BrickletCO2V2.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletCO2V2.CALLBACK_ALL_VALUES] = 'H h H'
        self.callback_formats[BrickletCO2V2.CALLBACK_CO2_CONCENTRATION] = 'H'
        self.callback_formats[BrickletCO2V2.CALLBACK_TEMPERATURE] = 'h'
        self.callback_formats[BrickletCO2V2.CALLBACK_HUMIDITY] = 'H'


    def get_all_values(self):
        """
        Returns all values measured by the CO2 Bricklet 2.0. The values are
        CO2 concentration (in ppm), temperature (in 0.01 °C)
        and humidity (in 0.01 %RH).

        If you want to get the values periodically, it is recommended to use the
        :cb:`All Values` callback. You can set the callback configuration
        with :func:`Set All Values Callback Configuration`.
        """
        return GetAllValues(*self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_ALL_VALUES, (), '', 'H h H'))

    def set_air_pressure(self, air_pressure):
        """
        The CO2 concentration (among other things) depends on the ambient air pressure.

        To increase the accuracy of the CO2 Bricklet 2.0 you can set the current air pressure.
        You use the :ref:`Barometer Bricklet 2.0 <barometer_v2_bricklet>` or the
        :ref:`Air Quality Bricklet <air_quality_bricklet>` to get the current air pressure.

        The expected unit of the ambient air pressure value is mbar.

        By default air pressure compensation is disabled. Once you set a value it
        will be used for compensation. You can turn the compensation off again by
        setting the value to 0.

        It is sufficient to update the value every few minutes.
        """
        air_pressure = int(air_pressure)

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_AIR_PRESSURE, (air_pressure,), 'H', '')

    def get_air_pressure(self):
        """
        Returns the ambient air pressure as set by :func:`Set Air Pressure`.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_AIR_PRESSURE, (), '', 'H')

    def set_temperature_offset(self, offset):
        """
        Sets a temperature offset with resolution 1/100°C. A offset of 10 will decrease
        the measured temperature by 0.1°C.

        If you install this Bricklet into an enclosure and you want to measure the ambient
        temperature, you may have to decrease the measured temperature by some value to
        compensate for the error because of the heating inside of the enclosure.

        We recommend that you leave the parts in the enclosure running for at least
        24 hours such that a temperature equilibrium can be reached. After that you can measure
        the temperature directly outside of enclosure and set the difference as offset.

        This temperature offset is used to calculate the relative humidity and
        CO2 concentration. In case the Bricklet is installed in an enclosure, we
        recommend to measure and set the temperature offset to improve the accuracy of
        the measurements.

        It is sufficient to set the temperature offset once. The offset is saved in
        non-volatile memory and is applied again after a power loss.
        """
        offset = int(offset)

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_TEMPERATURE_OFFSET, (offset,), 'H', '')

    def get_temperature_offset(self):
        """
        Returns the temperature offset as set by
        :func:`Set Temperature Offset`.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_TEMPERATURE_OFFSET, (), '', 'H')

    def set_all_values_callback_configuration(self, period, value_has_to_change):
        """
        The period in ms is the period with which the :cb:`All Values`
        callback is triggered periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after at least one of the values has changed. If the values didn't
        change within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        The default value is (0, false).
        """
        period = int(period)
        value_has_to_change = bool(value_has_to_change)

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_ALL_VALUES_CALLBACK_CONFIGURATION, (period, value_has_to_change), 'I !', '')

    def get_all_values_callback_configuration(self):
        """
        Returns the callback configuration as set by
        :func:`Set All Values Callback Configuration`.
        """
        return GetAllValuesCallbackConfiguration(*self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_ALL_VALUES_CALLBACK_CONFIGURATION, (), '', 'I !'))

    def get_co2_concentration(self):
        """
        Returns CO2 concentration in ppm.


        If you want to get the value periodically, it is recommended to use the
        :cb:`CO2 Concentration` callback. You can set the callback configuration
        with :func:`Set CO2 Concentration Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_CO2_CONCENTRATION, (), '', 'H')

    def set_co2_concentration_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`CO2 Concentration` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`CO2 Concentration` callback.

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

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c H H', '')

    def get_co2_concentration_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set CO2 Concentration Callback Configuration`.
        """
        return GetCO2ConcentrationCallbackConfiguration(*self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_CO2_CONCENTRATION_CALLBACK_CONFIGURATION, (), '', 'I ! c H H'))

    def get_temperature(self):
        """
        Returns temperature in steps of 0.01 °C.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Temperature` callback. You can set the callback configuration
        with :func:`Set Temperature Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_TEMPERATURE, (), '', 'h')

    def set_temperature_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Temperature` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Temperature` callback.

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

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_TEMPERATURE_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c h h', '')

    def get_temperature_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Temperature Callback Configuration`.
        """
        return GetTemperatureCallbackConfiguration(*self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_TEMPERATURE_CALLBACK_CONFIGURATION, (), '', 'I ! c h h'))

    def get_humidity(self):
        """
        Returns relative humidity in steps of 0.01 %RH.


        If you want to get the value periodically, it is recommended to use the
        :cb:`Humidity` callback. You can set the callback configuration
        with :func:`Set Humidity Callback Configuration`.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_HUMIDITY, (), '', 'H')

    def set_humidity_callback_configuration(self, period, value_has_to_change, option, min, max):
        """
        The period in ms is the period with which the :cb:`Humidity` callback is triggered
        periodically. A value of 0 turns the callback off.

        If the `value has to change`-parameter is set to true, the callback is only
        triggered after the value has changed. If the value didn't change
        within the period, the callback is triggered immediately on change.

        If it is set to false, the callback is continuously triggered with the period,
        independent of the value.

        It is furthermore possible to constrain the callback with thresholds.

        The `option`-parameter together with min/max sets a threshold for the :cb:`Humidity` callback.

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

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_HUMIDITY_CALLBACK_CONFIGURATION, (period, value_has_to_change, option, min, max), 'I ! c H H', '')

    def get_humidity_callback_configuration(self):
        """
        Returns the callback configuration as set by :func:`Set Humidity Callback Configuration`.
        """
        return GetHumidityCallbackConfiguration(*self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_HUMIDITY_CALLBACK_CONFIGURATION, (), '', 'I ! c H H'))

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
        return GetSPITFPErrorCount(*self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_SPITFP_ERROR_COUNT, (), '', 'I I I I'))

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

        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_BOOTLOADER_MODE, (mode,), 'B', 'B')

    def get_bootloader_mode(self):
        """
        Returns the current bootloader mode, see :func:`Set Bootloader Mode`.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_BOOTLOADER_MODE, (), '', 'B')

    def set_write_firmware_pointer(self, pointer):
        """
        Sets the firmware pointer for :func:`Write Firmware`. The pointer has
        to be increased by chunks of size 64. The data is written to flash
        every 4 chunks (which equals to one page of size 256).

        This function is used by Brick Viewer during flashing. It should not be
        necessary to call it in a normal user program.
        """
        pointer = int(pointer)

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_WRITE_FIRMWARE_POINTER, (pointer,), 'I', '')

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

        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_WRITE_FIRMWARE, (data,), '64B', 'B')

    def set_status_led_config(self, config):
        """
        Sets the status LED configuration. By default the LED shows
        communication traffic between Brick and Bricklet, it flickers once
        for every 10 received data packets.

        You can also turn the LED permanently on/off or show a heartbeat.

        If the Bricklet is in bootloader mode, the LED is will show heartbeat by default.
        """
        config = int(config)

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_SET_STATUS_LED_CONFIG, (config,), 'B', '')

    def get_status_led_config(self):
        """
        Returns the configuration as set by :func:`Set Status LED Config`
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_STATUS_LED_CONFIG, (), '', 'B')

    def get_chip_temperature(self):
        """
        Returns the temperature in °C as measured inside the microcontroller. The
        value returned is not the ambient temperature!

        The temperature is only proportional to the real temperature and it has bad
        accuracy. Practically it is only useful as an indicator for
        temperature changes.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_CHIP_TEMPERATURE, (), '', 'h')

    def reset(self):
        """
        Calling this function will reset the Bricklet. All configurations
        will be lost.

        After a reset you have to create new device objects,
        calling functions on the existing ones will result in
        undefined behavior!
        """
        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_RESET, (), '', '')

    def write_uid(self, uid):
        """
        Writes a new UID into flash. If you want to set a new UID
        you have to decode the Base58 encoded UID string into an
        integer first.

        We recommend that you use Brick Viewer to change the UID.
        """
        uid = int(uid)

        self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_WRITE_UID, (uid,), 'I', '')

    def read_uid(self):
        """
        Returns the current UID as an integer. Encode as
        Base58 to get the usual string version.
        """
        return self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_READ_UID, (), '', 'I')

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletCO2V2.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

CO2V2 = BrickletCO2V2 # for backward compatibility
