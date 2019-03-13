#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

ft.py: Entry file for flash and test tool

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import sys

from PyQt5 import Qt, QtWidgets, QtCore

from mainwindow import MainWindow

class FlashTestApplication(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        QtWidgets.QApplication.__init__(self, *args, **kwargs)

def main():
    argv = sys.argv

    ft = FlashTestApplication(argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(ft.exec_())

if __name__ == "__main__":
    main()
