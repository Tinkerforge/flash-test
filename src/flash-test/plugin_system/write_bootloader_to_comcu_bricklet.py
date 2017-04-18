#!/usr/bin/env python3

CONFIG_BAUDRATE   = 115200
CONFIG_TTY        = '/dev/ttyUSB0'
CONFIG_UID_MASTER = ('6qzRzc', '6kP6n3', '6Jprbj')
CONFIG_UID_IQR    = '555'

USBDEVFS_RESET = 21780

MASK_NONE  = 0b0000
MASK_TX    = 0b1000
MASK_POWER = 0b0010
MASK_DATA  = 0b0001

import time
import os
import sys
from subprocess import Popen, PIPE
import fcntl
from zipfile import ZipFile

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_industrial_quad_relay import BrickletIndustrialQuadRelay
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

    iqr = BrickletIndustrialQuadRelay(uid_iqr, ipcon)
    master = BrickMasterFlashAdapterXMC(uid_master, ipcon)

    try:
        xmc_write_firmwares_to_ram(firmware, master)
    except Exception as e:
        print(str(e))
        return

    i = 2
    while True:
        if i == 2:
            iqr.set_value(MASK_NONE | MASK_DATA)
            time.sleep(0.1)
            iqr.set_value(MASK_POWER)
            i = 0

        i += 1
        try:
            time.sleep(0.01)
            xmc_flash(master)
            break
        except Exception as e:
            print(str(e))

    print('Done')
        
    iqr.set_value(MASK_POWER)

    master.reset()
    
    ipcon.disconnect()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please give .zbin as parameter')
    else:
        relay_flash(CONFIG_BAUDRATE, CONFIG_TTY, sys.argv[1], CONFIG_UID_IQR)