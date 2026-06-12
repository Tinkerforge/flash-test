#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

HOST = "localhost"
PORT = 4223

try:
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', 'evse_v4_tester_id.txt'), 'rb') as f:
        tester_id = f.read().decode('utf-8').split('\n')[0].strip()
except FileNotFoundError:
    tester_id = '1'

if tester_id == '1':
    UID_IAI1 = "2j4j" # PP, CP
    UID_IO41 = "2hqd" # LED R, G, B, Start Flash
    UID_IQR1 = "2iqi" # Front Switch
    UID_IQR2 = "2iqd" # PP 13A, 20A, 32A, 63A
    UID_IQR3 = "2iq7" # Enable, 230V, Contactor Check 0, Contactor Check 1
    UID_IQR4 = "2dVZ" # CP B, CP C, CP D
    UID_IACI = "28xF" # Lsw0, Lsw1
    UID_LED  = "2f2U" # RGB LED Strip -> 13 LEDs

    UID_IAI2 = "2j4i" # 3.3V, 5V
    UID_IAI3 = "2j4g" # 12V, -12V
    UID_IO42 = "2hrZ" # G0, G1, G2, PRST
    UID_IDR  = "2jhj" # NC 12V sthutdown
else:
    pass

from .tinkerforge.ip_connection import IPConnection
from .tinkerforge.bricklet_evse_v2 import BrickletEVSEV2

from .tinkerforge.bricklet_industrial_dual_analog_in_v2 import BrickletIndustrialDualAnalogInV2
from .tinkerforge.bricklet_io4_v2                       import BrickletIO4V2
from .tinkerforge.bricklet_industrial_quad_relay_v2     import BrickletIndustrialQuadRelayV2
from .tinkerforge.bricklet_industrial_dual_ac_in        import BrickletIndustrialDualACIn
from .tinkerforge.bricklet_led_strip_v2                 import BrickletLEDStripV2
from .tinkerforge.bricklet_industrial_dual_relay        import BrickletIndustrialDualRelay

import time
import sys
import threading

log = print

class EVSEV4Tester:
    def __init__(self, log_func=None, start_func=None):
        if log_func:
            global log
            log = log_func

        self.start_func = start_func
        self.ipcon = IPConnection()

        self.led_animation_thread = None
        self.led_animation_stop_event = None

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
        self.iai1 = BrickletIndustrialDualAnalogInV2(UID_IAI1, self.ipcon)
        self.io41 = BrickletIO4V2(UID_IO41,                    self.ipcon)
        self.iqr1 = BrickletIndustrialQuadRelayV2(UID_IQR1,    self.ipcon)
        self.iqr2 = BrickletIndustrialQuadRelayV2(UID_IQR2,    self.ipcon)
        self.iqr3 = BrickletIndustrialQuadRelayV2(UID_IQR3,    self.ipcon)
        self.iqr4 = BrickletIndustrialQuadRelayV2(UID_IQR4,    self.ipcon)
        self.iaci = BrickletIndustrialDualACIn(UID_IACI,       self.ipcon)
        self.led  = BrickletLEDStripV2(UID_LED,                self.ipcon)
        self.iai2 = BrickletIndustrialDualAnalogInV2(UID_IAI2, self.ipcon)
        self.iai3 = BrickletIndustrialDualAnalogInV2(UID_IAI3, self.ipcon)
        self.io42 = BrickletIO4V2(UID_IO42,                    self.ipcon)
        self.idr  = BrickletIndustrialDualRelay(UID_IDR,       self.ipcon)

        devices = [self.iai1, self.io41, self.iqr1, self.iqr2, self.iqr3, self.iqr4, self.iaci, self.led, self.iai2, self.iai3, self.io42, self.idr]

        for device in devices:
            device.set_response_expected_all(True)
            device.reset()

        time.sleep(0.5)

        self.iai1.set_sample_rate(self.iai1.SAMPLE_RATE_4_SPS)
        self.io41.register_callback(self.io41.CALLBACK_INPUT_VALUE, self.cb_io4_value)
        self.io41.set_input_value_callback_configuration(3, 100, True)
        self.led.set_chip_type(self.led.CHIP_TYPE_WS2812)
        self.led.set_channel_mapping(self.led.CHANNEL_MAPPING_GRB)
        self.set_led(0, 0, 255)

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
        self.stop_led_animation()
        self.led.set_led_values(0, [r, g, b]*13)

    def stop_led_animation(self):
        if self.led_animation_thread != None:
            self.led_animation_stop_event.set()
            self.led_animation_thread.join()
            self.led_animation_thread = None
            self.led_animation_stop_event = None

    def set_led_animation(self, animation):
        self.stop_led_animation()

        if animation == 0:
            self.led_animation_stop_event = threading.Event()
            self.led_animation_thread = threading.Thread(target=self.led_animation_moving_blue, args=(self.led_animation_stop_event,), daemon=True)
            self.led_animation_thread.start()

    def led_animation_moving_blue(self, stop_event):
        trail = [16, 64, 255, 64, 16]
        position = 0
        while not stop_event.is_set():
            values = [0, 0, 0] * 13
            for offset, blue in enumerate(trail):
                i = (position + offset - 2) % 13
                values[i*3 + 2] = blue

            self.led.set_led_values(0, values)

            position = (position + 1) % 13
            stop_event.wait(0.05)

    def set_evse_led(self, r, g, b):
        ret = -1
        if r:   ret = self.evse.set_indicator_led(255, 10000, 0, 255, 255)
        elif g: ret = self.evse.set_indicator_led(255, 10000, 120, 255, 255)
        elif b: ret = self.evse.set_indicator_led(255, 10000, 240, 255, 255)
        log("Set EVSE LED {0} {1} {2}, ret {3}".format(r, g, b, ret))

    def get_evse_led(self):
        value = self.io41.get_value()
        value = [not value[0], not value[1], not value[2]]
        log("Get EVSE LED {0} {1} {2}".format(*value))
        return value

    def press_button(self, value):
        self.iqr1.set_selected_value(0, value)
        log("Press button {0}".format(value))

    def set_230v(self, value):
        self.iqr3.set_selected_value(1, value)
        self.idr.set_selected_value(0, value)
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

        uptime_start = 0
        uptime_end = 0

        while True:
            state = self.evse.get_low_level_state()
            if uptime_start == 0:
                uptime_start = state.uptime

            if state.gpio[11] == active:
                break

            uptime_end = state.uptime

            if time.time() - start > 10:
                log("Contactor GPIO to did not become {0}active...".format("" if active else "in"))
                return (False, 0)

            time.sleep(0.01)

        log("Done")
        return (True, uptime_end - uptime_start)

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
        return self.iai1.get_voltage(1)

    def get_pp_pe_voltage(self):
        return self.iai1.get_voltage(0)

    def get_p3v3(self):
        return self.iai2.get_voltage(0)

    def get_p5v(self):
        return self.iai2.get_voltage(1)

    def get_p12v(self):
        return self.iai3.get_voltage(0)

    def get_m12v(self):
        return self.iai3.get_voltage(1)

    def exit(self, value):
        if value == 0:
            self.set_led(0, 255, 0)
        else:
            self.set_led(255, 0, 0)
        self.iqr1.set_value([False]*4)
        self.iqr2.set_value([False]*4)
        self.iqr3.set_value([False]*4)
        self.iqr4.set_value([False]*4)
