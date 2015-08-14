#!/bin/sh

rm -rf download.tinkerforge.com firmwares
wget --no-parent -r http://download.tinkerforge.com/firmwares/
mv download.tinkerforge.com/firmwares firmwares
rm -rf download.tinkerforge.com
