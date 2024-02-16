#!/usr/bin/env python3

import traceback
import time
import sys
from zipfile import ZipFile

try:
    from .tinkerforge.ip_connection import IPConnection
    from .tinkerforge.brick_master import BrickMaster
except ImportError:
    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.brick_master import BrickMaster

global_uid_master = None

def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    global global_uid_master
    if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
        return

    if (hardware_version[0] == 3) and (position == '0') and (uid != '6ss6Tw'):
        global_uid_master = uid

def xmc_write_firmwares_to_ram(zbin, master, non_standard_print = None):
    if non_standard_print != None:
        print_func = non_standard_print
    else:
        print_func = print

    try:
        zf = ZipFile(zbin, 'r')
    except:
        raise Exception('Bricklet', 'Konnte Bricklet Plugin nicht öffnen:\n\n' + traceback.format_exc())

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
        raise Exception('Bricklet', 'Konnte Firmware nicht in zbin finden')

    if bootloader == None:
        raise Exception('Bricklet', 'Konnte Bootloader nicht in zbin finden')

    if bootstrapper == None:
        raise Exception('Bricklet', 'Konnte Bootstrapper nicht in zbin finden')

    ret = master.set_bricklet_xmc_flash_config(0, len(bootstrapper), 0, [0]*52) # Start Bootstrapper Write
    if ret.return_value != 0:
        raise Exception('Bricklet', 'Start Boostrapper Schreib-Fehler: ' + str(ret.return_value))


    print_func('Schreibe Bootstrapper')
    bootstrapper_chunks = [bootstrapper[i:i + 64] for i in range(0, len(bootstrapper), 64)]
    bootstrapper_chunks[-1].extend([0]*(64-len(bootstrapper_chunks[-1])))
    for chunk in bootstrapper_chunks:
        ret = master.set_bricklet_xmc_flash_data(chunk)
        if ret != 0:
            raise Exception('Bricklet', 'Bootstrapper schreiben Chunk Fehler: ' + str(ret))


    ret = master.set_bricklet_xmc_flash_config(1, len(bootloader), 0, [0]*52) # Start Bootloader Write
    if ret.return_value != 0:
        raise Exception('Bricklet', 'Start Bootloader Schreib-Fehler: ' + str(ret.return_value))

    print_func('Schreibe Bootloader')
    bootloader_chunks = [bootloader[i:i + 64] for i in range(0, len(bootloader), 64)]
    for chunk in bootloader_chunks:
        ret = master.set_bricklet_xmc_flash_data(chunk)
        if ret != 0:
            raise Exception('Bricklet', 'Bootloader schreiben Chunk Fehler: ' + str(ret))

def xmc_flash_bootloader(zbin, uid_master=None, non_standard_print=None, power_off_duration=None):
    if non_standard_print != None:
        print_func = non_standard_print
    else:
        print_func = print

    if power_off_duration == None:
        power_off_duration = 0.25

    ipcon = IPConnection()
    ipcon.connect('localhost', 4223)

    if uid_master == None:
        global global_uid_master
        ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)
        ipcon.enumerate()

        start = time.time()
        while time.time() - start < 1:
            if global_uid_master != None:
                break
    
            time.sleep(0.1)

        if global_uid_master == None:
            raise Exception('Bricklet', 'Could not find program master')

        uid_master = global_uid_master

    master = BrickMaster(uid_master, ipcon)
    identity = master.get_identity()
    print_func('Using Master {0}'.format(str(identity.uid)))

    xmc_write_firmwares_to_ram(zbin, master)

    errors = set()
    time.sleep(0.2)
    i = 10
    start = time.time()

    ret = True
    while True:
        if time.time() - start > 3:
            print_func('Timeout beim Bootloader schreiben')
            ret = False
            break

        if i == 10:
            if len(errors) > 0:
                print_func('Errors: {0}'.format(str(errors)))
                errors.clear()
            master.set_bricklets_enabled(False)
            time.sleep(power_off_duration)
            master.set_bricklets_enabled(True)
            i = 0

        i += 1
        try:
            time.sleep(0.001)
            ret = master.set_bricklet_xmc_flash_config(2, 0, 0, [0]*52)
            if ret.return_value == 0:
                break
                
            errors.add(str(ret.return_value))
        except Exception as e:
            errors.add(str(e))

    if ret != False:
        print_func('Done (try ' + str(i) + ')')
        
    master.set_bricklets_enabled(True)

    master.reset()
    
    ipcon.disconnect()

    return ret

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please give .zbin as parameter')
    else:
        xmc_flash_bootloader(sys.argv[1])
