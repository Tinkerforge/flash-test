#!/usr/bin/env python3

import traceback
import time
from zipfile import ZipFile
def xmc_write_firmwares_to_ram(zbin, master, non_standard_print = None):
    if non_standard_print != None:
        print_func = non_standard_print
    else:
        print_func = print

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
    if ret.return_value != 0:
        raise Exception('Bricklet', 'Start Boostrapper Write Error: ' + str(ret.return_value))


    print_func('Write Bootstrapper')
    bootstrapper_chunks = [bootstrapper[i:i + 64] for i in range(0, len(bootstrapper), 64)]
    bootstrapper_chunks[-1].extend([0]*(64-len(bootstrapper_chunks[-1])))
    for chunk in bootstrapper_chunks:
        ret = master.set_flash_adapter_xmc_data(chunk)
        if ret != 0:
            raise Exception('Bricklet', 'Write Bootstrapper Chunk Error: ' + str(ret))


    ret = master.set_flash_adapter_xmc_config(1, len(bootloader), 0, [0]*52) # // Start Bootstrapper Write
    if ret.return_value != 0:
        raise Exception('Bricklet', 'Start Bootloader Write Error: ' + str(ret.return_value))

    print_func('Write Bootloader')
    bootloader_chunks = [bootloader[i:i + 64] for i in range(0, len(bootloader), 64)]
    for chunk in bootloader_chunks:
        ret = master.set_flash_adapter_xmc_data(chunk)
        if ret != 0:
            raise Exception('Bricklet', 'Write Bootloader Chunk Error: ' + str(ret))


def xmc_flash(master):
    ret = master.set_flash_adapter_xmc_config(2, 0, 0, [0]*52)
    if ret.return_value != 0:
        raise Exception('Bricklet', 'Flash Error: ' + str(ret.return_value))


