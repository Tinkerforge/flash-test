#!/bin/sh

echo "Connect Bricklet to port D on Master Brick"
/usr/bin/python3 $(dirname $(readlink -f $0))/src/flash-test/plugin_system/xmc_flash_bootloader.py "$@"
sleep 2.5
/usr/bin/python3 $(dirname $(readlink -f $0))/src/flash-test/plugin_system/xmc_flash_firmware.py "$@"
