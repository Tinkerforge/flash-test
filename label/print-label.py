#!/usr/bin/python3 -u

import os
import sys
import re
import argparse
import socket
from datetime import datetime

PRINTER_HOST = '192.168.178.244'
PRINTER_PORT = 9100

NAME_PLACEHOLDER = b'Industrial Dual Analog In Bricklet 2.0'

SKU_PLACEHOLDER = b'556677'

DATE_PLACEHOLDER = b'1999-10-12'

UID_PLACEHOLDER = b'XXYYZZ'

VERSION_PLACEHOLDER = b'2.17.5'

COPIES_FORMAT = '^C{0}\r'

def print_label(name, sku, date, uid, version, copies, stdout):
    # check copies
    if copies < 1 or copies > 20:
        raise Exception('Invalid copies: {0}'.format(copies))

    # check date
    datetime.strptime(date, '%Y-%m-%d')

    # check version
    if re.match(r'^(\d+.\d+.\d+|-)$', version) == None:
        raise Exception('Invalid version: {0}'.format(version))

    # read EZPL file
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'label.prn'), 'rb') as f:
        template = f.read()

    if b'^D0\r' not in template or b'^D0\r' not in template:
        raise Exception('EZPL file is using wrong print mode setting')

    template = template.replace(b'^D0\r', b'^D1\r')

    if template.find(b'^H13\r') < 0:
        raise Exception('EZPL file is using wrong darkness setting')

    if template.find(b'^O1\r') < 0:
        raise Exception('EZPL file is using wrong dispenser setting')

    if template.find(b'^E8\r') < 0:
        raise Exception('EZPL file is using wrong tear-off setting')

    # patch name
    if template.find(NAME_PLACEHOLDER) < 0:
        raise Exception('Name placeholder missing in EZPL file')

    template = template.replace(NAME_PLACEHOLDER, name.encode('ascii'))

    # patch SKU
    if template.find(SKU_PLACEHOLDER) < 0:
        raise Exception('SKU placeholder missing in EZPL file')

    template = template.replace(SKU_PLACEHOLDER, sku.encode('ascii'))

    # patch date
    if template.find(DATE_PLACEHOLDER) < 0:
        raise Exception('Date placeholder missing in EZPL file')

    template = template.replace(DATE_PLACEHOLDER, date.encode('ascii'))

    # patch UID
    if template.find(UID_PLACEHOLDER) < 0:
        raise Exception('UID placeholder missing in EZPL file')

    template = template.replace(UID_PLACEHOLDER, uid.encode('ascii'))

    # patch version
    if template.find(VERSION_PLACEHOLDER) < 0:
        raise Exception('Version placeholder missing in EZPL file')

    template = template.replace(VERSION_PLACEHOLDER, version.encode('ascii'))

    # patch copies
    copies_command = COPIES_FORMAT.format(1).encode('ascii')

    if template.find(copies_command) < 0:
        raise Exception('Copies command missing in EZPL file')

    template = template.replace(copies_command, COPIES_FORMAT.format(copies).encode('ascii'))

    # print label
    if stdout:
        sys.stdout.buffer.write(template)
        sys.stdout.buffer.flush()
    else:
        with socket.create_connection((PRINTER_HOST, PRINTER_PORT)) as s:
            s.send(template)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('name')
    parser.add_argument('sku')
    parser.add_argument('date')
    parser.add_argument('uid')
    parser.add_argument('version')
    parser.add_argument('-c', '--copies', type=int, default=1)
    parser.add_argument('-s', '--stdout', action='store_true')

    args = parser.parse_args()

    assert args.copies > 0

    print_label(args.name, args.sku, args.date, args.uid, args.version, args.copies, args.stdout)

if __name__ == '__main__':
    main()
