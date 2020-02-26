#!/usr/bin/env python3

CONFIG_BAUDRATE   = 115200
CONFIG_TTY        = '/dev/ttyUSB0'
CONFIG_UID_MASTER = ('6qzRzc', '6kP6n3', '6Jprbj', '6DdMSG')
CONFIG_UID_IQR    = '555'

USBDEVFS_RESET = 21780

MASK_NONE = (False, False, False, False)
MASK_POWER = (False, False, True, True)

import time
import os
import sys
from subprocess import Popen, PIPE
import fcntl
from zipfile import ZipFile

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_quad_relay_v2 import BrickletIndustrialQuadRelayV2
from tinkerforge.brick_master_flash_adapter_xmc import BrickMasterFlashAdapterXMC
from xmc_flash_by_master import xmc_flash, xmc_write_firmwares_to_ram

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
    master = BrickMasterFlashAdapterXMC(uid_master, ipcon)

    use_half_duplex = 0
    if firmware.endswith('industrial-encoder-bricklet-firmware.zbin'):
        use_half_duplex = 1

    try:
        xmc_write_firmwares_to_ram(firmware, master)
    except Exception as e:
        print(str(e))
        return

    errors = set()
    time.sleep(0.2)
    i = 10
    while True:
        if i == 10:
            if len(errors) > 0:
                print(errors)
                errors.clear()
            iqr.set_value(MASK_NONE)
            time.sleep(0.05)
            iqr.set_value(MASK_POWER)
            i = 0

        i += 1
        try:
            time.sleep(0.001)
            xmc_flash(master, use_half_duplex)
            break
        except Exception as e:
            errors.add(str(e))

    print('Done (try ' + str(i) + ')')
        
    iqr.set_value(MASK_POWER)

    master.reset()
    
    ipcon.disconnect()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please give .zbin as parameter')
    else:
        relay_flash(CONFIG_BAUDRATE, CONFIG_TTY, sys.argv[1], CONFIG_UID_IQR)
