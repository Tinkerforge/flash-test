#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

HOST     = "localhost"
PORT     = 4223

try:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'evse_v3_tester_id.txt'), 'rb') as f:
        tester_id = f.read().decode('utf-8').split('\n')[0].strip()
except FileNotFoundError:
    tester_id = '1'

if tester_id == '1':
    UID_IDAI = "23RC" # PP, CP
    UID_IO4  = "27q9" # LED R, G, B, Start Flash
    UID_IQR1 = "RVG"  # Front Switch
    UID_IQR2 = "RNW"  # PP 13A, 20A, 32A, 63A
    UID_IQR3 = "RzF"  # Enable, 230V, Contactor Check 0, Contactor Check 1
    UID_IQR4 = "2dVY" # CP B, CP C, CP D
    UID_IACI = "28Af" # Lsw0, Lsw1
    UID_LED  = "29aw" # RGB LED
else:
    UID_IDAI = "28rh" # PP, CP
    UID_IO4  = "27ny" # LED R, G, B, Start Flash
    UID_IQR1 = "2bmU" # Front Switch
    UID_IQR2 = "2bnK" # PP 13A, 20A, 32A, 63A
    UID_IQR3 = "2bmW" # Enable, 230V, Contactor Check 0, Contactor Check 1
    UID_IQR4 = "2dVX" # CP B, CP C, CP D
    UID_IACI = "28zG" # Lsw0, Lsw1
    UID_LED  = "298V" # RGB LED

from .tinkerforge.ip_connection import IPConnection
from .tinkerforge.bricklet_evse_v2 import BrickletEVSEV2

from .tinkerforge.bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
from .tinkerforge.bricklet_io4_v2                       import BrickletIO4V2
from .tinkerforge.bricklet_industrial_quad_relay_v2     import BrickletIndustrialQuadRelayV2
from .tinkerforge.bricklet_industrial_dual_ac_in        import BrickletIndustrialDualACIn
from .tinkerforge.bricklet_rgb_led_v2                   import BrickletRGBLEDV2

import time
import sys

log = print

class EVSEV3Tester:
    def __init__(self, log_func=None, start_func=None):
        if log_func:
            global log
            log = log_func

        self.start_func = start_func
        self.ipcon = IPConnection()

    def setup(self):
        try:
            self.ipcon.disconnect()
        except:
            pass

        self.ipcon.connect(HOST, PORT)
        self.ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, self.cb_enumerate)
        self.ipcon.enumerate()

        self.evse_uid = None
        self.evse = None
        self.idai = BrickletIndustrialDualAnalogInV2(UID_IDAI, self.ipcon)
        self.io4  = BrickletIO4V2(UID_IO4,                     self.ipcon)
        self.iqr1 = BrickletIndustrialQuadRelayV2(UID_IQR1,    self.ipcon)
        self.iqr2 = BrickletIndustrialQuadRelayV2(UID_IQR2,    self.ipcon)
        self.iqr3 = BrickletIndustrialQuadRelayV2(UID_IQR3,    self.ipcon)
        self.iqr4 = BrickletIndustrialQuadRelayV2(UID_IQR4,    self.ipcon)
        self.iaci = BrickletIndustrialDualACIn(UID_IACI,       self.ipcon)
        self.led  = BrickletRGBLEDV2(UID_LED,                  self.ipcon)

        devices = [self.idai, self.io4, self.iqr1, self.iqr2, self.iqr3, self.iqr4, self.iaci, self.led]

        for device in devices:
            device.set_response_expected_all(True)
            device.reset()

        time.sleep(0.5)

        self.idai.set_sample_rate(self.idai.SAMPLE_RATE_4_SPS)
        self.io4.register_callback(self.io4.CALLBACK_INPUT_VALUE, self.cb_io4_value)
        self.io4.set_input_value_callback_configuration(3, 100, True)
        self.led.set_status_led_config(self.led.STATUS_LED_CONFIG_OFF)

    def cb_enumerate(self, uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type):
        if device_identifier == BrickletEVSEV2.DEVICE_IDENTIFIER:
            self.evse_uid = uid
            self.evse = BrickletEVSEV2(uid, self.ipcon)

    def cb_io4_value(self, channel, changed, value):
        if channel == 3 and changed:
            self.set_led(0, 0, 0)

            if not value and self.start_func != None:
                self.start_func()

    def find_evse(self):
        self.evse = None
        self.ipcon.enumerate()

        log("Trying to find EVSE Bricklet...")
        start = time.time()

        while self.evse == None:
            if time.time() - start > 10:
                log("Could not find EVSE Bricklet")
                return False

            time.sleep(0.1)

        log("Found EVSE Bricklet: {0}".format(self.evse_uid))
        return True

    def set_led(self, r, g, b):
        self.led.set_rgb_value(r, g, b)

    def set_evse_led(self, r, g, b):
        ret = -1
        if r:   ret = self.evse.set_indicator_led(255, 10000, 0, 255, 255)
        elif g: ret = self.evse.set_indicator_led(255, 10000, 120, 255, 255)
        elif b: ret = self.evse.set_indicator_led(255, 10000, 240, 255, 255)
        log("Set EVSE LED {0} {1} {2}, ret {3}".format(r, g, b, ret))

    def get_evse_led(self):
        value = self.io4.get_value()
        value = [not value[0], not value[1], not value[2]]
        log("Get EVSE LED {0} {1} {2}".format(*value))
        return value

    def press_button(self, value):
        self.iqr1.set_selected_value(0, value)
        log("Press button {0}".format(value))

    def set_230v(self, value):
        self.iqr3.set_selected_value(1, value)
        log("Set 230V to {0}".format(value))

    # Live = True
    def set_contactor_fb(self, value):
        log('Set contactor fb {0}'.format(value))

        self.iqr3.set_selected_value(2, value)
        self.iqr3.set_selected_value(3, value)

    def set_cp_pe_resistor(self, r2700, r1300, r270):
        value = list(self.iqr4.get_value())
        value[1] = r2700
        value[2] = r1300
        value[3] = r270
        self.iqr4.set_value(value)

        l = []
        if r2700: l.append("2700 Ohm")
        if r1300: l.append("1300 Ohm")
        if r270:  l.append("270 Ohm")

        log("Set CP/PE resistor: " + ', '.join(l))

    def set_pp_pe_resistor(self, r1500, r680, r220, r100):
        value = [r1500, r680, r220, r100]
        self.iqr2.set_value(value)

        l = []
        if r1500: l.append("1500 Ohm")
        if r680:  l.append("680 Ohm")
        if r220:  l.append("220 Ohm")
        if r100:  l.append("110 Ohm")

        log("Set PP/PE resistor: " + ', '.join(l))

    def wait_for_contactor_gpio(self, active):
        log("Waiting for contactor GPIO to become {0}active...".format("" if active else "in"))

        start = time.time()
        counter = 0

        while True:
            state = self.evse.get_low_level_state()

            if state.gpio[11] == active:
                break

            if counter > 100:
                counter = 0

                if time.time() - start > 10:
                    log("Contactor GPIO to did not become {0}active...".format("" if active else "in"))
                    return False

            counter += 1
            time.sleep(0.01)

        log("Done")
        return True

    def wait_for_button_gpio(self, active):
        log("Waiting for button GPIO to become {0}active...".format("" if active else "in"))

        start = time.time()
        while True:
            state = self.evse.get_low_level_state()
            if (not state.gpio[5]) == active:
                break
            if time.time() - start > 10:
                log("Button GPIO to did not become {0}active...".format("" if active else "in"))
                return False
            time.sleep(0.1)

        log("Done")
        return True

    def set_max_charging_current(self, current):
        self.evse.set_charging_slot(5, current, True, False)

    def shutdown_input_enable(self, enable):
        self.iqr3.set_selected_value(0, enable)

    def get_hardware_version(self):
        return self.evse.get_hardware_configuration().evse_version

    def get_energy_meter_data(self):
        a = self.evse.get_energy_meter_values()
        b = self.evse.get_all_energy_meter_values()
        c = self.evse.get_hardware_configuration()
        d = self.evse.get_energy_meter_errors()
        return (a, b, c, d)

    def get_cp_pe_voltage(self):
        return self.idai.get_voltage(1)

    def get_pp_pe_voltage(self):
        return self.idai.get_voltage(0)

    def exit(self, value):
        if value == 0:
            self.set_led(0, 255, 0)
        else:
            self.set_led(255, 0, 0)
        self.iqr1.set_value([False]*4)
        self.iqr2.set_value([False]*4)
        self.iqr3.set_value([False]*4)
        self.iqr4.set_value([False]*4)
