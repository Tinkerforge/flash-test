#!/bin/bash
pushd src > /dev/null
python3 build_ui.py
popd > /dev/null
cd src/flash-test
exec ./ft.py "$@"
