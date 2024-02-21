#!/usr/bin/env python3

from zipfile import ZipFile
import sys
import time
import traceback

try:
    from .tinkerforge.ip_connection import IPConnection
    from .tinkerforge.bricklet_unknown import BrickletUnknown
    from .tinkerforge.brick_master import BrickMaster
except ImportError:
    from tinkerforge.ip_connection import IPConnection
    from tinkerforge.bricklet_unknown import BrickletUnknown
    from tinkerforge.brick_master import BrickMaster

found_uid = None
def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type):
    # allow HATs
    if (str(device_identifier) == '111') or (str(device_identifier) == '112'):
        pass
    # search for bricklets only
    elif not str(device_identifier).startswith('2'):
        return

    global found_uid
    found_uid = uid

def get_first_bricklet_uid(ipcon):
    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)
    ipcon.enumerate()
    for i in range(1000):
        if found_uid != None:
            return found_uid
        time.sleep(0.01)

def xmc_flash_firmware(zbin, uid_bricklet=None):
    start = time.time()
    try:
        print('Starting bootloader mode')


        try:
            zf = ZipFile(zbin, 'r')
        except:
            print('Konnte Bricklet Plugin nicht öffnen:\n\n' + traceback.format_exc())
            return False, None

        plugin_data = None
        for name in zf.namelist():
            if name.endswith('firmware.bin'):
                plugin_data = zf.read(name)
                break

        if plugin_data == None:
            print('Konnte Firmware in zbin nicht finden')
            return False, None

        # Now convert plugin to list of bytes
        plugin = plugin_data
        regular_plugin_upto = -1
        for i in reversed(range(4, len(plugin)-12)):
            if plugin[i] == 0x12 and plugin[i-1] == 0x34 and plugin[i-2] == 0x56 and plugin[i-3] == 0x78:
                regular_plugin_upto = i
                break

        if regular_plugin_upto == -1:
            print('Konnte "magic number" in Firmware nicht finden')

        ipcon = IPConnection()
        ipcon.connect('localhost', 4223)
        if uid_bricklet == None:
            uid_bricklet = get_first_bricklet_uid(ipcon)
            if uid_bricklet == None:
                print('Could not find any Bricklet')
                return

        print('Using UID: ' + uid_bricklet)

        device = BrickletUnknown(uid_bricklet, ipcon)

        device.set_bootloader_mode(device.BOOTLOADER_MODE_BOOTLOADER)
        counter = 0
        last_exc_tup = None
        while True:
            try:
                if device.get_bootloader_mode() == device.BOOTLOADER_MODE_BOOTLOADER:
                    break
            except:
                last_exc_tup = sys.exc_info()

            if counter == 10:
                print('Gerät nicht im Bootloader-Modus nach 2,5s.')
                traceback.print_exception(*last_exc_tup)
                return False, None

            time.sleep(0.25)
            counter += 1

        num_packets = len(plugin)//64
        index_list = range(num_packets)

        for _ in range(2):
            if _ == 1:
                index_list = range(num_packets)

            print('Schreibe Firmware: ' + name)
            to_write = str(len(index_list) - 1)
            for position in index_list:
                start = position*64
                end   = (position+1)*64
                print('Schreibe Firmware: ' + str(position) + '/' + to_write)
                device.set_write_firmware_pointer(start)
                device.write_firmware(plugin[start:end])

            print('Wechsle vom Bootloader-Modus in den Firmware-Modus')

            mode_ret = device.set_bootloader_mode(device.BOOTLOADER_MODE_FIRMWARE)
            if mode_ret != 0 and mode_ret != 2: # 0 = ok, 2 = no change
                error_str = ''
                if mode_ret == 1:
                    error_str = 'Invalid mode (Error 1)'
                elif mode_ret == 3:
                    error_str = 'Entry function not present (Error 3)'
                elif mode_ret == 4:
                    error_str = 'Device identifier incorrect (Error 4)'
                elif mode_ret == 5:
                    error_str = 'CRC Mismatch (Error 5)'
                else: # unkown error case
                    error_str = 'Error ' + str(mode_ret)

                # In case of CRC Mismatch we try a second time
                if mode_ret == 5:
                    continue

                print('Konnte nicht vom Bootloader-Modus in den Firmware-Modus wechseln: ' + error_str)
                return False, None

            # Everything OK, we dont have to try a second time
            break

        counter = 0
        last_exc_tup = None
        while True:
            try:
                bootloader_mode = device.get_bootloader_mode()
                if bootloader_mode == device.BOOTLOADER_MODE_FIRMWARE:
                    break
            except:
                last_exc_tup = sys.exc_info()

            if counter == 10:
                print('Gerät nicht im Firmware-Modus nach 25s.')
                traceback.print_exception(*last_exc_tup)
                return False, None

            time.sleep(0.25)
            counter += 1

        print('Firmware geschrieben und gestartet')
    except:
        traceback.print_exception()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please give .zbin as parameter')
    else:
        xmc_flash_firmware(sys.argv[1])
