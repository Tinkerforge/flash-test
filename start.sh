#!/bin/sh
pushd src
python build_ui.py
popd
cd src/flash-test
exec ./ft.py
