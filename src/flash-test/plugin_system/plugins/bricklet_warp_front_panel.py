# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2024 Olaf Lüke <olaf@tinkerforge.com>

bricklet_warp_front_panel.py: WARP Front Panel plugin

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

from PyQt5 import Qt, QtGui, QtCore

from ..tinkerforge.bricklet_warp_front_panel import BrickletWARPFrontPanel
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator
from threading import Thread
import time
import os

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde WARP Energy Manager Bricklet mit Port D des Master Bricks 3.0
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Warte bis externe Flash gesflasht ist.
5. Prüfe das LED-Farbe zwischen grün, rot und gelb wechselt
6. Drücke Taster, prüfe das QR-Code auftaucht auf Display
7. Das Bricklet ist fertig
8. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_led_state = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_led_state != None:
            self.cbe_led_state.set_period(0)

    def get_device_identifier(self):
        return BrickletWARPFrontPanel.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletWARPFrontPanel.DEVICE_URL_PART), power_off_duration=10, try_count=1000)

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_led_state != None:
            self.cbe_led_state.set_period(0)

        self.wfp = BrickletWARPFrontPanel(device_information.uid, self.get_ipcon())
        if self.wfp.get_bootloader_mode() != BrickletWARPFrontPanel.BOOTLOADER_MODE_FIRMWARE:
            return

        self.flash_started = False
        self.flash_status = 'Flashprozess für externen Flash noch nicht gestartet'

        self.cbe_led_state = CallbackEmulator(self.wfp.get_led_state, self.cb_get_led_state, ignore_last_data=True)
        self.cbe_led_state.set_period(500)

        self.show_device_information(device_information)

    def flash_flashmap(self):
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))

        file_directory = os.path.dirname(os.path.realpath(__file__))
        flashmap = os.path.join(file_directory, '..', '..', '..', '..', 'extras', 'warp_front_panel_flash_map.bin')

        with open(flashmap, 'rb') as f:
            index = 0
            self.flash_status = "Erase flash " + str(self.wfp.erase_flash())
            time.sleep(1)
            self.wfp.set_flash_index(0, 0)
            data = f.read()
            data_len = len(data)
            for index, data in enumerate(chunker(data, 64)):
                if len(data) < 64:
                    data = data + [0]*(64-len(data))
                ret = self.wfp.set_flash_data(data)
                while ret.status != BrickletWARPFrontPanel.FLASH_STATUS_OK:
                    self.flash_status = "Warte {0}/{1}".format(index*64, data_len)
                    ret = self.wfp.set_flash_data(data)
                    time.sleep(0.002)
                else:
                    self.flash_status = "Schreibe {0}/{1}".format(index*64, data_len)
        self.flash_status = "Fertig"

    def cb_get_led_state(self, value):
        self.wfp.set_led_state(self.wfp.LED_PATTERN_ON, (value.color + 1) % 3)
        if self.flash_status == "Fertig":
            self.mw.set_value_okay("Flashen abgeschlossen")
        else:
            self.mw.set_value_action(self.flash_status)

        if not self.flash_started:
            Thread(target=self.flash_flashmap).start()
            self.flash_started = True