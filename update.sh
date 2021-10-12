#!/bin/bash -e

echo "Aktualisiere Firmwares..."
rm -rf download.tinkerforge.com firmwares
ln -s ../firmwares firmwares
pushd firmwares
git pull
popd

echo ""
echo "Aktualisiere Software..."
git pull

echo ""
echo "Baue GUI und Plugin-Liste neu..."
pushd src
python3 build_ui.py
popd

echo ""
echo "Update erfolgreich durchgeführt!"

echo ""
read -p "Enter drücken zum Beenden " dummy
