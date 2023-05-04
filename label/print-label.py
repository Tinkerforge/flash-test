#!/usr/bin/python3 -u

import os
import sys
import re
import argparse
import socket
from datetime import datetime

NAME_1_PLACEHOLDER = b'Industrial Dual Analog In Bricklet 2.0'
NAME_2_PLACEHOLDER = b'Ethernet Master Extension (without PoE)'
NAME_3_PLACEHOLDER = b'Board-to-Board Connector 30 Pin (Brick Bottom 4.85mm)'
NAME_4a_PLACEHOLDER = b'Starter Kit: Server Room Monitoring (Assembly Kit,'
NAME_4b_PLACEHOLDER = b'None-Stand-Alone)'

NAME_1_MAX_LENGTH = 35
NAME_2_MAX_LENGTH = 50
NAME_3_MAX_LENGTH = 55

SKU_PLACEHOLDER = b'556677'

DATE_PLACEHOLDER = b'1999-10-12'

UID_PLACEHOLDER = b'XXYYZZ'

VERSION_PLACEHOLDER = b'2.17.5'

COPIES_FORMAT = '^C{0}\r'


def get_tf_printer_host(task):
    import re
    import os
    import sys

    x = re.compile(r'^\s*([A-Za-z0-9_-]+)\s+([0-9\.]+)\s*$')

    try:
        with open(os.path.expanduser('~/tf_printer_host.txt'), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                m = x.match(line)

                if m == None:
                    print('WARNING: Invalid line in ~/tf_printer_host.txt: {0}'.format(repr(line)))

                    continue

                other_task = m.group(1)
                other_host = m.group(2)

                if other_task != task:
                    continue

                return other_host
    except FileNotFoundError:
        pass

    print('ERROR: Printer host for task {0} not found in ~/tf_printer_host.txt')

    sys.exit(1)


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
    if len(name) <= NAME_1_MAX_LENGTH:
        template_filename = 'label1.prn'
        name_placeholders = [NAME_1_PLACEHOLDER]
        name_parts = [name]
    elif len(name) <= NAME_2_MAX_LENGTH:
        template_filename = 'label2.prn'
        name_placeholders = [NAME_2_PLACEHOLDER]
        name_parts = [name]
    elif len(name) <= NAME_3_MAX_LENGTH:
        template_filename = 'label3.prn'
        name_placeholders = [NAME_3_PLACEHOLDER]
        name_parts = [name]
    else:
        template_filename = 'label4.prn'
        name_placeholders = [NAME_4a_PLACEHOLDER, NAME_4b_PLACEHOLDER]
        name_parts = [[]]

        for name_part in name.split(' '):
            if len(' '.join(name_parts[-1] + [name_part])) <= NAME_3_MAX_LENGTH:
                name_parts[-1].append(name_part)
            else:
                name_parts.append([name_part])

        name_parts = [' '.join(x) for x in name_parts]

        if len(name_parts) < 2:
            name_parts.append('')

    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), template_filename), 'rb') as f:
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
    for name_placeholder, name_part in zip(name_placeholders, name_parts):
        if template.find(name_placeholder) < 0:
            raise Exception('Name placeholder missing in EZPL file')

        template = template.replace(name_placeholder, name_part.encode('latin1'))

    # patch SKU
    if template.find(SKU_PLACEHOLDER) < 0:
        raise Exception('SKU placeholder missing in EZPL file')

    template = template.replace(SKU_PLACEHOLDER, sku.encode('latin1'))

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
        with socket.create_connection((get_tf_printer_host('esd-bag'), 9100)) as s:
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
