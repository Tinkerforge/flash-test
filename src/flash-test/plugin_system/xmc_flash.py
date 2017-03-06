#!/usr/bin/env python3

# Test program for simple bootstrapper/firmware flashing
# Copy bootloader as "bl.bin" in software folder.
# Configure variables below as necessary

CONFIG_BAUDRATE = 115200
CONFIG_TTY      = '/dev/ttyACM0'
CONFIG_FIRMWARE = 'bl.bin'


import traceback
import serial
import time
from zipfile import ZipFile

BSL_START  = [0x00]
BSL_ASC_F  = [0x6C]
BSL_ASC_H  = [0x12]
BSL_ENC_F  = [0x93]
BSL_ENC_H  = [0xED]

BSL_BR_OK  = [0xF0]
BSL_ID     = [0x5D]
BSL_ENC_ID = [0xA2]
BSL_BR_OK  = [0xF0]
BSL_OK     = [0x01]
BSL_NOK    = [0x02]

class BrickletSerial:
    baudrate = 19200
    port = 'ABC'
    timeout = 0.25

    def __init__(self):
        pass

    def open(self):
        pass

    def write(self, data):
        pass

    def read(self, length):
        pass

    def flush(self):
        pass

def xmc_flash(baudrate, tty, zbin, use_bricklet = False, non_standard_print = None):
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
            bootloader = zf.read(name)
        elif name.endswith('bootstrapper.bin'):
            bootstrapper = zf.read(name)

    if firmware == None:
        raise Exception('Bricklet', 'Could not find firmware in zbin')

    if bootloader == None:
        raise Exception('Bricklet', 'Could not find firmware in zbin')

    if bootstrapper == None:
        raise Exception('Bricklet', 'Could not find firmware in zbin')

    if use_bricklet:
        Serial = BrickletSerial
    else:
        Serial = serial.Serial

    with Serial() as s:
        s.baudrate = baudrate
        s.port = tty
        s.timeout = 0.2
        s.open()

        print_func("Opening " + str(s.name))

        s.write(BSL_START)
        s.write(BSL_ASC_F)
        ret = s.read(1)
        if len(ret) < 1:
            raise Exception("Handshake error: No answer")
        elif ord(ret) != BSL_ID[0]:
            raise Exception("Handshake error, received: " + hex(ord(ret)))

        length = len(bootstrapper)
        length_write = [length & 0xFF, (length >> 8) & 0xFF, (length >> 16) & 0xFF, (length >> 24) & 0xFF]

        print_func("Write bootstrapper length")
        s.write(length_write)
        ret = s.read(1)

        if len(ret) < 1:
            raise Exception("Write bootstrapper length error: No answer")
        elif ord(ret) != BSL_OK[0]:
            raise Exception("Write bootstrapper length error, received: " + hex(ord(ret)))

        print_func("Write bootstrapper")
        s.write(bootstrapper)
        ret = s.read(1)

        if len(ret) < 1:
            raise Exception("Write bootstrapper error: No answer")
        elif ord(ret) != BSL_OK[0]:
            raise Exception("Write bootstrapper error, received: " + hex(ord(ret)))

        print_func("Write bootstrapper done")
    
        s.flush()

        pages = len(bootloader)//256
        for page in range(pages):
            print_func("Write bootloader page " + str(page))
            s.write(bootloader[page*256:(page+1)*256])
            
            ret_crc = s.read(1)
            crc = 0
            for i in range(256):
                crc = crc ^ bootloader[page*256+i]

            if len(ret_crc) < 1:
                raise Exception("Did not get CRC as answer for page write")

            if crc != ord(ret_crc):
                print_func("Read CRC (mcu vs calc): {0} vs {1}".format(ord(ret_crc), crc))
                raise Exception("CRC Error")

        print_func("Write bootloader done")


if __name__ == '__main__':
    xmc_flash(CONFIG_BAUDRATE, CONFIG_TTY, CONFIG_FIRMWARE)
