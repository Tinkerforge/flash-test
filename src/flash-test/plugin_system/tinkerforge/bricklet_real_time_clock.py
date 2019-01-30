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

GetDateTime = namedtuple('DateTime', ['year', 'month', 'day', 'hour', 'minute', 'second', 'centisecond', 'weekday'])
GetAlarm = namedtuple('Alarm', ['month', 'day', 'hour', 'minute', 'second', 'weekday', 'interval'])
GetIdentity = namedtuple('Identity', ['uid', 'connected_uid', 'position', 'hardware_version', 'firmware_version', 'device_identifier'])

class BrickletRealTimeClock(Device):
    """
    Battery-backed real-time clock
    """

    DEVICE_IDENTIFIER = 268
    DEVICE_DISPLAY_NAME = 'Real-Time Clock Bricklet'
    DEVICE_URL_PART = 'real_time_clock' # internal

    CALLBACK_DATE_TIME = 10
    CALLBACK_ALARM = 11


    FUNCTION_SET_DATE_TIME = 1
    FUNCTION_GET_DATE_TIME = 2
    FUNCTION_GET_TIMESTAMP = 3
    FUNCTION_SET_OFFSET = 4
    FUNCTION_GET_OFFSET = 5
    FUNCTION_SET_DATE_TIME_CALLBACK_PERIOD = 6
    FUNCTION_GET_DATE_TIME_CALLBACK_PERIOD = 7
    FUNCTION_SET_ALARM = 8
    FUNCTION_GET_ALARM = 9
    FUNCTION_GET_IDENTITY = 255

    WEEKDAY_MONDAY = 1
    WEEKDAY_TUESDAY = 2
    WEEKDAY_WEDNESDAY = 3
    WEEKDAY_THURSDAY = 4
    WEEKDAY_FRIDAY = 5
    WEEKDAY_SATURDAY = 6
    WEEKDAY_SUNDAY = 7
    ALARM_MATCH_DISABLED = -1
    ALARM_INTERVAL_DISABLED = -1

    def __init__(self, uid, ipcon):
        """
        Creates an object with the unique device ID *uid* and adds it to
        the IP Connection *ipcon*.
        """
        Device.__init__(self, uid, ipcon)

        self.api_version = (2, 0, 1)

        self.response_expected[BrickletRealTimeClock.FUNCTION_SET_DATE_TIME] = BrickletRealTimeClock.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRealTimeClock.FUNCTION_GET_DATE_TIME] = BrickletRealTimeClock.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRealTimeClock.FUNCTION_GET_TIMESTAMP] = BrickletRealTimeClock.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRealTimeClock.FUNCTION_SET_OFFSET] = BrickletRealTimeClock.RESPONSE_EXPECTED_FALSE
        self.response_expected[BrickletRealTimeClock.FUNCTION_GET_OFFSET] = BrickletRealTimeClock.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRealTimeClock.FUNCTION_SET_DATE_TIME_CALLBACK_PERIOD] = BrickletRealTimeClock.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRealTimeClock.FUNCTION_GET_DATE_TIME_CALLBACK_PERIOD] = BrickletRealTimeClock.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRealTimeClock.FUNCTION_SET_ALARM] = BrickletRealTimeClock.RESPONSE_EXPECTED_TRUE
        self.response_expected[BrickletRealTimeClock.FUNCTION_GET_ALARM] = BrickletRealTimeClock.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickletRealTimeClock.FUNCTION_GET_IDENTITY] = BrickletRealTimeClock.RESPONSE_EXPECTED_ALWAYS_TRUE

        self.callback_formats[BrickletRealTimeClock.CALLBACK_DATE_TIME] = 'H B B B B B B B q'
        self.callback_formats[BrickletRealTimeClock.CALLBACK_ALARM] = 'H B B B B B B B q'


    def set_date_time(self, year, month, day, hour, minute, second, centisecond, weekday):
        """
        Sets the current date (including weekday) and the current time with hundredths
        of a second resolution.

        Possible value ranges:

        * Year: 2000 to 2099
        * Month: 1 to 12 (January to December)
        * Day: 1 to 31
        * Hour: 0 to 23
        * Minute: 0 to 59
        * Second: 0 to 59
        * Centisecond: 0 to 99
        * Weekday: 1 to 7 (Monday to Sunday)

        If the backup battery is installed then the real-time clock keeps date and
        time even if the Bricklet is not powered by a Brick.

        The real-time clock handles leap year and inserts the 29th of February
        accordingly. But leap seconds, time zones and daylight saving time are not
        handled.
        """
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        centisecond = int(centisecond)
        weekday = int(weekday)

        self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_SET_DATE_TIME, (year, month, day, hour, minute, second, centisecond, weekday), 'H B B B B B B B', '')

    def get_date_time(self):
        """
        Returns the current date (including weekday) and the current time of the
        real-time clock with hundredths of a second resolution.
        """
        return GetDateTime(*self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_GET_DATE_TIME, (), '', 'H B B B B B B B'))

    def get_timestamp(self):
        """
        Returns the current date and the time of the real-time clock converted to
        milliseconds. The timestamp has an effective resolution of hundredths of a
        second.
        """
        return self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_GET_TIMESTAMP, (), '', 'q')

    def set_offset(self, offset):
        """
        Sets the offset the real-time clock should compensate for in 2.17 ppm steps
        between -277.76 ppm (-128) and +275.59 ppm (127).

        The real-time clock time can deviate from the actual time due to the frequency
        deviation of its 32.768 kHz crystal. Even without compensation (factory
        default) the resulting time deviation should be at most ±20 ppm (±52.6
        seconds per month).

        This deviation can be calculated by comparing the same duration measured by the
        real-time clock (``rtc_duration``) an accurate reference clock
        (``ref_duration``).

        For best results the configured offset should be set to 0 ppm first and then a
        duration of at least 6 hours should be measured.

        The new offset (``new_offset``) can be calculated from the currently configured
        offset (``current_offset``) and the measured durations as follow::

          new_offset = current_offset - round(1000000 * (rtc_duration - ref_duration) / rtc_duration / 2.17)

        If you want to calculate the offset, then we recommend using the calibration
        dialog in Brick Viewer, instead of doing it manually.

        The offset is saved in the EEPROM of the Bricklet and only needs to be
        configured once.
        """
        offset = int(offset)

        self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_SET_OFFSET, (offset,), 'b', '')

    def get_offset(self):
        """
        Returns the offset as set by :func:`Set Offset`.
        """
        return self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_GET_OFFSET, (), '', 'b')

    def set_date_time_callback_period(self, period):
        """
        Sets the period in ms with which the :cb:`Date Time` callback is triggered
        periodically. A value of 0 turns the callback off.

        The :cb:`Date Time` Callback is only triggered if the date or time changed
        since the last triggering.

        The default value is 0.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        period = int(period)

        self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_SET_DATE_TIME_CALLBACK_PERIOD, (period,), 'I', '')

    def get_date_time_callback_period(self):
        """
        Returns the period as set by :func:`Set Date Time Callback Period`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        return self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_GET_DATE_TIME_CALLBACK_PERIOD, (), '', 'I')

    def set_alarm(self, month, day, hour, minute, second, weekday, interval):
        """
        Configures a repeatable alarm. The :cb:`Alarm` callback is triggered if the
        current date and time matches the configured alarm.

        Setting a parameter to -1 means that it should be disabled and doesn't take part
        in the match. Setting all parameters to -1 disables the alarm completely.

        For example, to make the alarm trigger every day at 7:30 AM it can be
        configured as (-1, -1, 7, 30, -1, -1, -1). The hour is set to match 7 and the
        minute is set to match 30. The alarm is triggered if all enabled parameters
        match.

        The interval has a special role. It allows to make the alarm reconfigure itself.
        This is useful if you need a repeated alarm that cannot be expressed by matching
        the current date and time. For example, to make the alarm trigger every 23
        seconds it can be configured as (-1, -1, -1, -1, -1, -1, 23). Internally the
        Bricklet will take the current date and time, add 23 seconds to it and set the
        result as its alarm. The first alarm will be triggered 23 seconds after the
        call. Because the interval is not -1, the Bricklet will do the same again
        internally, take the current date and time, add 23 seconds to it and set that
        as its alarm. This results in a repeated alarm that triggers every 23 seconds.

        The interval can also be used in combination with the other parameters. For
        example, configuring the alarm as (-1, -1, 7, 30, -1, -1, 300) results in an
        alarm that triggers every day at 7:30 AM and is then repeated every 5 minutes.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        weekday = int(weekday)
        interval = int(interval)

        self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_SET_ALARM, (month, day, hour, minute, second, weekday, interval), 'b b b b b b i', '')

    def get_alarm(self):
        """
        Returns the alarm configuration as set by :func:`Set Alarm`.

        .. versionadded:: 2.0.1$nbsp;(Plugin)
        """
        return GetAlarm(*self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_GET_ALARM, (), '', 'b b b b b b i'))

    def get_identity(self):
        """
        Returns the UID, the UID where the Bricklet is connected to,
        the position, the hardware and firmware version as well as the
        device identifier.

        The position can be 'a', 'b', 'c' or 'd'.

        The device identifier numbers can be found :ref:`here <device_identifier>`.
        |device_identifier_constant|
        """
        return GetIdentity(*self.ipcon.send_request(self, BrickletRealTimeClock.FUNCTION_GET_IDENTITY, (), '', '8s 8s c 3B 3B H'))

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

RealTimeClock = BrickletRealTimeClock # for backward compatibility
