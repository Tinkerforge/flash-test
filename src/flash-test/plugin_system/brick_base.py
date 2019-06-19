# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

brick_base.py: Base for Bricks

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

from plugin_system.plugin_base import PluginBase
from plugin_system.samba import SAMBA, SAMBAException
from serial import SerialException

from PyQt5 import QtCore

import os
import time
import threading

def get_brick_firmware_filename(name):
    file_directory = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(file_directory, '..', '..', '..', 'firmwares', 'bricks', name, 'brick_' + name + '_firmware_latest.bin')

class Progress:
    def __init__(self, mw):
        self.mw = mw
        self.m = 0

    def update(self, value):
        if value % 10 or value == self.m:
            self.mw.set_tool_status_action("Fortschritt: " + str(value) + '/' + str(self.m))
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')
            self.mw.set_value_normal('-')

    def reset(self, t, m):
        self.m = m

class FlashThread(QtCore.QThread):
    flash_signal = QtCore.pyqtSignal([str])

    def __init__(self, mw, bb, filename):
        QtCore.QThread.__init__(self)
        self.mw = mw
        self.bb = bb
        self.filename = filename
        self.stopped = False

    def run(self):
        while not self.stopped:
            self.flash_signal.emit(self.filename)
            time.sleep(0.5)

    def start(self):
        self.stopped = False
        QtCore.QThread.start(self)

    def stop(self):
        self.stopped = True

class BrickBase(PluginBase):
    def __init__(self, *args):
        PluginBase.__init__(self, *args)

        self.flash_thread = FlashThread(self.mw, self, self.FIRMWARE_FILENAME)
        self.flash_thread.flash_signal.connect(self.flash)
        self.is_flashing = False

    def flash(self, filename):
        if self.is_flashing:
            return

        self.is_flashing = True
        firmware = None

        try:
            with open(filename, "rb") as f:
                firmware = f.read()
        except IOError as e:
            self.mw.set_tool_status_error("Konnte Firmware Datei nicht lesen: {0}".format(e.strerror))
            self.mw.button_continue.show()
            return

        retry = True
        retry_counter = 0
        success = False

        while retry and retry_counter < 2:
            retry = False
            retry_counter += 1

            try:
                samba = SAMBA('/dev/ttyACM0', Progress(self.mw))
                samba.flash(firmware, None, False)
                success = True
            except SerialException as e:
                self.mw.set_tool_status_normal("Aktuell kein Brick im Bootloader-Modus")
                self.is_flashing = False
                return
            except SAMBAException as e:
                if 'No permission to open serial port' in str(e):
                    time.sleep(1)
                    retry = True
                else:
                    self.mw.set_tool_status_error('Konnte Brick nicht flashen: {0}'.format(e))
                    self.mw.button_continue.show()
                    return
            except Exception as e:
                self.mw.set_tool_status_error('Konnte Brick nicht flashen: {0}'.format(e))
                self.mw.button_continue.show()
                return

        if not success:
            self.mw.set_tool_status_error('Konnte Brick nicht flashen: Kein Zugriff auf /dev/ttyACM0 möglich?')
            self.mw.button_continue.show()
            return

        self.mw.set_tool_status_okay("Brick geflasht")
        self.is_flashing = False

        self.mw.increase_flashed_count()

    def start(self):
        self.mw.button_flash.setEnabled(False)
        PluginBase.start(self)
        self.show_device_information(None, clear_value=True)
        self.is_flashing = False
        self.flash_thread.start()

    def show_device_information(self, device_information, clear_value=False):
        if device_information != None:
            self.mw.set_tool_status_okay("Firmware gefunden")
            self.mw.set_uid_status_okay("Aktuelle UID lautet " + device_information.uid)
            self.mw.set_flash_status_okay("Aktuelle Firmware Version lautet " + '.'.join([str(fw) for fw in device_information.firmware_version]))
        else:
            self.mw.set_tool_status_normal("Keine Firmware gefunden")
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('-')

        self.mw.button_continue.hide()
        self.is_flashing = False

        if clear_value:
            self.mw.set_value_normal('-')

    def stop(self):
        self.mw.button_flash.setEnabled(True)
        PluginBase.stop(self)
        self.flash_thread.stop()

    def continue_clicked(self):
        self.mw.button_continue.hide()
        self.is_flashing = False
