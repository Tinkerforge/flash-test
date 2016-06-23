# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2016 Matthias Bolte <matthias@tinkerforge.com>

extension_wifi_v2.py: WIFI Extension 2.0 plugin

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

from PyQt4 import Qt, QtGui, QtCore

from ..tinkerforge.brick_master import BrickMaster
from ..extension_base import ExtensionBase, get_extension_firmware_filename
from ..callback_emulator import CallbackEmulator
from ..esp_flash import ESPFlash

import time

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

class Plugin(ExtensionBase):
    TODO_TEXT = u"""\
1. Stecke WIFI Extension 2.0 auf Master Brick
2. Stecke Master Brick an USB
3. Warte bis Flash-Vorgang abgeschlossen wird
4. Warte bis WLAN-Verbindung hergestellt wird
5. Grüne LED muss blinken, blaue LED muss leuchten
6. Pinken Punkt mit Alkohol entfernen
7. Die Extension ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
8. Gehe zu 1
"""
    def start(self, device_information):
        self.device_information = None
        self.master = None

        ExtensionBase.start(self, device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickMaster.EXTENSION_TYPE_WIFI2*10000 + BrickMaster.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        self.device_information = device_information
        self.master = BrickMaster(device_information.uid, self.get_ipcon())

        self.mw.set_tool_status_normal('Master Brick gefunden')

        for x in range(10):
            QtGui.QApplication.processEvents()
            time.sleep(0.01)

        try:
            present = self.master.is_wifi2_present()
        except:
            self.mw.set_tool_status_normal('Fehler beim Abfragen der Extension aufgetreten')
            return

        if present:
            self.mw.set_tool_status_action('Versuche WLAN-Verbindung aufzubauen')
            self.mw.set_uid_status_normal('-')

            try:
                self.mw.set_flash_status_okay('Aktuelle Firmware Version lautet ' + '.'.join([str(fw) for fw in self.master.get_wifi2_firmware_version()]))
            except:
                self.mw.set_flash_status_error('Fehler beim Abfragen der Firmware Version aufgetreten')

            self.mw.set_value_normal('-')

            QtCore.QTimer.singleShot(0.1, self.try_connect)
        else:
            self.mw.set_tool_status_action('Verbinde mit Bootloader')
            self.mw.set_uid_status_normal('-')
            self.mw.set_flash_status_normal('Keine Firmware gefunden')
            self.mw.set_value_normal('-')

            self.flash_extension()

    def flash_extension(self):
        try:
            with open(get_extension_firmware_filename('wifi_v2', extension='zbin'), 'rb') as f:
                firmware = f.read()
        except IOError as e:
            self.mw.set_tool_status_error("Konnte Firmware Datei nicht lesen: {0}".format(e.strerror))
            return

        try:
            ESPFlash(self.master, Progress(self.mw)).flash(firmware)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.mw.set_tool_status_error("Fehler beim Flashen: {0}".format(e))
            return

        self.mw.set_tool_status_okay('Extension geflasht')

        for x in range(10):
            QtGui.QApplication.processEvents()
            time.sleep(0.01)

        self.mw.set_tool_status_action('Setze Extension-Typ')

        self.master.set_extension_type(0, BrickMaster.EXTENSION_TYPE_WIFI2)

        for x in range(10):
            QtGui.QApplication.processEvents()
            time.sleep(0.01)

        try:
            while self.master.get_extension_type(0) != BrickMaster.EXTENSION_TYPE_WIFI2:
                self.master.set_extension_type(0, BrickMaster.EXTENSION_TYPE_WIFI2)

                for x in range(10):
                    QtGui.QApplication.processEvents()
                    time.sleep(0.01)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.mw.set_tool_status_error("Fehler beim Setzen des Extension-Typ: {0}".format(e))
            return

        self.master.reset()
        self.mw.set_tool_status_action('Extension-Typ gesetzt, starte Master Brick neu')

    def try_connect(self):
        i = 0
        range_to = 100

        for i in range(range_to):
            try:
                status = self.master.get_wifi2_status()

                if status.client_status == 5: # got IP address
                    i = 0
                    break
            except:
                pass

            for x in range(10):
                QtGui.QApplication.processEvents()
                time.sleep(0.01)

        if i == range_to-1:
            self.master.reset()
            self.mw.set_tool_status_error('Konnte keine WLAN-Verbindung aufbauen, starte Master Brick neu')
            return

        self.mw.set_tool_status_okay('WLAN-Verbindung aufgebaut. Fertig!')
