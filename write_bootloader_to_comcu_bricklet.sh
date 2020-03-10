#!/bin/sh

/usr/bin/python3 $(dirname $(readlink -f $0))/src/flash-test/plugin_system/xmc_flash_bootloader.py "$@"
