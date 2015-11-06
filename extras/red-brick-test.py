#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# store this file in /home/tf

import subprocess
import os
import time

extensions = {
'0': 'FEHLT',
'1': 'Chibi',
'2': 'RS485',
'3': 'WIFI',
'4': 'Ethernet',
'5': 'WIFI 2.0'
}

if __name__ == '__main__':
    print('==== lsusb =======================================================')

    output = subprocess.check_output('lsusb').decode('utf-8')

    for line in output.split('\n'):
        if 'Linux Foundation 3.0 root hub' in line or \
           'Linux Foundation 2.0 root hub' in line or \
           'Linux Foundation 1.1 root hub' in line or \
           'Linux Foundation 1.0 root hub' in line:
            continue

        print(line)

    print('==== ping ========================================================')

    try:
        output = subprocess.check_output(['ping', '-c', '1', 'google.de'], stderr=subprocess.STDOUT).decode('utf-8')
        print(output)
    except Exception as e:
        print('FEHLER: ' + str(e))

    print('\n==== extension 0 ===============================================')

    found = False
    try:
        with open('/tmp/extension_position_0.conf') as f:
            for line in f.read().split('\n'):
                parts = line.split(' = ')

                if parts[0] == 'type':
                    print(extensions[parts[1]])
                    found = True
                    break

        if not found:
            print('FEHLT')
    except Exception as e:
        print('FEHLER: ' + str(e))

    print('\n==== extension 1 ===============================================')

    found = False
    try:
        with open('/tmp/extension_position_1.conf') as f:
            for line in f.read().split('\n'):
                parts = line.split(' = ')

                if parts[0] == 'type':
                    print(extensions[parts[1]])
                    found = True
                    break

        if not found:
            print('FEHLT')
    except Exception as e:
        print('FEHLER: ' + str(e))
