#!/bin/sh -e

echo "Lade Firmwares herunter..."
rm -rf download.tinkerforge.com firmwares
wget --no-parent -r http://download.tinkerforge.com/firmwares/
mv download.tinkerforge.com/firmwares firmwares
rm -rf download.tinkerforge.com

echo ""
echo "Aktualisiere Software..."
git pull

echo ""
echo "Baue GUI und Plugin-Liste neu..."
pushd src
python build_ui.py
popd

echo ""
echo "Update erfolgreich durchgeführt!"
