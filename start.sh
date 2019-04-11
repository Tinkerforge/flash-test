#!/bin/bash
pushd src
python3 build_ui.py
popd
cd src/flash-test
exec ./ft.py
