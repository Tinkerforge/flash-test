#!/bin/sh

/usr/bin/python3 $(dirname $(readlink -f $0))/src/flash-test/plugin_system/write_bootloader_to_comcu_bricklet.py "$@"
