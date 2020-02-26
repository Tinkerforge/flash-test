#!/usr/bin/env python3

CONFIG_BAUDRATE   = 115200
CONFIG_TTY        = '/dev/ttyUSB0'
CONFIG_UID_MASTER = ('6qzRzc', '6kP6n3', '6Jprbj')
CONFIG_UID_IQR    = '555'

USBDEVFS_RESET = 21780

MASK_NONE = (False, False, False, False)
MASK_POWER = (False, True, False, False)
MASK_POWER_AND_DATA = (True, True, False, False)

import time
import os
import sys
from subprocess import Popen, PIPE
import fcntl

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from tinkerforge.brick_master import BrickMaster
from xmc_flash import xmc_flash

uid_master = None

def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    global uid_master
    if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
        return

    if uid in CONFIG_UID_MASTER:
        uid_master = uid

def relay_flash(baudrate, tty, firmware, uid_iqr):
    global uid_master
    ipcon = IPConnection()
    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)
    ipcon.connect('localhost', 4223)
    ipcon.enumerate()

    start = time.time()
    while time.time() - start < 1:
        if uid_master != None:
            break
 
        time.sleep(0.1)

    if uid_master == None:
        print('Could not find program master')
        return

    iqr = BrickletIndustrialQuadRelayV2(uid_iqr, ipcon)
    master = BrickMaster(uid_master, ipcon)

    i = 2
    while True:
        if i == 2:
            master.get_chibi_error_log()
            iqr.set_value(MASK_NONE)
            time.sleep(0.1)
            iqr.set_value(MASK_POWER_AND_DATA)
            i = 0

        i += 1
        try:
            time.sleep(0.01)
            xmc_flash(baudrate, tty, firmware)
            break
        except Exception as e:
            print(str(e))
        
    iqr.set_value(MASK_POWER)

    master.reset()

    ipcon.disconnect()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please give .zbin as parameter')
    else:
        relay_flash(CONFIG_BAUDRATE, CONFIG_TTY, sys.argv[1], CONFIG_UID_IQR)
