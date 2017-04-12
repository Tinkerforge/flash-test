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
from xmc_flash_by_master import xmc_flash

uid_master = None

def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    global uid_master
    if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
        return

    if uid in CONFIG_UID_MASTER:
        uid_master = uid

def xmc_write_firmwares_to_ram(zbin, master):
    try:
        zf = ZipFile(zbin, 'r')
    except:
        raise Exception('Bricklet', 'Could not open Bricklet plugin:\n\n' + traceback.format_exc())

    firmware = None
    bootloader = None
    bootstrapper = None
    for name in zf.namelist():
        if name.endswith('firmware.bin'):
            firmware = zf.read(name)
        elif name.endswith('bootloader.bin'):
            bootloader = list(zf.read(name))
        elif name.endswith('bootstrapper.bin'):
            bootstrapper = list(zf.read(name))

    if firmware == None:
        raise Exception('Bricklet', 'Could not find firmware in zbin')

    if bootloader == None:
        raise Exception('Bricklet', 'Could not find bootloader in zbin')

    if bootstrapper == None:
        raise Exception('Bricklet', 'Could not find bootstrapper in zbin')

    ret = master.set_flash_adapter_xmc_config(0, len(bootstrapper), 0, [0]*52) # // Start Bootstrapper Write
    print('Start Boostrapper Write Error: ' + str(ret.return_value))


    print('Write Bootstrapper')
    bootstrapper_chunks = [bootstrapper[i:i + 64] for i in range(0, len(bootstrapper), 64)]
    bootstrapper_chunks[-1].extend([0]*(64-len(bootstrapper_chunks[-1])))
    for chunk in bootstrapper_chunks:
        ret = master.set_flash_adapter_xmc_data(chunk)
        if ret != 0:
            print('Write Bootstrapper Chunk Error: ' + str(ret))


    ret = master.set_flash_adapter_xmc_config(1, len(bootloader), 0, [0]*52) # // Start Bootstrapper Write
    print('Start Bootloader Write Error: ' + str(ret.return_value))

    print('Write Bootloader')
    bootloader_chunks = [bootloader[i:i + 64] for i in range(0, len(bootloader), 64)]
    for chunk in bootloader_chunks:
        ret = master.set_flash_adapter_xmc_data(chunk)
        if ret != 0:
            print('Write Bootloader Chunk Error: ' + str(ret))

def xmc_flash(master):
    ret = master.set_flash_adapter_xmc_config(2, 0, 0, [0]*52)
    if ret.return_value != 0:
        print('Flash Error: ' + str(ret.return_value))
    return ret.return_value

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


    xmc_write_firmwares_to_ram(firmware, master)

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
            if xmc_flash(master) != 0:
                continue
            break
        except Exception as e:
            import traceback
            traceback.print_exc()

    print('Done')
        
    iqr.set_value(MASK_POWER)

    master.reset()
    
    ipcon.disconnect()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please give .zbin as parameter')
    else:
        relay_flash(CONFIG_BAUDRATE, CONFIG_TTY, sys.argv[1], CONFIG_UID_IQR)
