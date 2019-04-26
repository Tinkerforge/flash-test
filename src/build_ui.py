#!/usr/bin/env python3

import os

def system(command):
    if os.system(command) != 0:
        exit(1)

system("python3 pyuic5-fixed.py -o flash-test/ui_mainwindow.py flash-test/ui/mainwindow.ui")
system("python3 build_plugin_list.py")
