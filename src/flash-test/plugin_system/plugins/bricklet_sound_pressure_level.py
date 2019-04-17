# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2018 Olaf Lüke <olaf@tinkerforge.com>

bricklet_sound_pressure_level.py: Sound Pressure Level plugin

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

from ..tinkerforge.bricklet_sound_pressure_level import BrickletSoundPressureLevel
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Sound Pressure Level Bricklet mit 2.0 Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe Werte: dB Wert sollte unter 60 sein bei normalen nebengeräuschen und über 60
   wenn du auf den Tisch neben das Bricklet klopfst. Wert wird grün wenn beides einmal erreicht wurde.
5. Das Bricklet ist fertig, in kleine ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_decibel = None
        self.cbe_decibel_below_60 = True
        self.cbe_decibel_above_60 = True

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        super().stop()
        if self.cbe_decibel != None:
            self.cbe_decibel.set_period(0)

    def get_device_identifier(self):
        return BrickletSoundPressureLevel.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletSoundPressureLevel.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_decibel != None:
            self.cbe_decibel.set_period(0)

        self.sound_pressure_level = BrickletSoundPressureLevel(device_information.uid, self.get_ipcon())
        if self.sound_pressure_level.get_bootloader_mode() != BrickletSoundPressureLevel.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_decibel_below_60 = False
        self.cbe_decibel_above_60 = False

        self.cbe_decibel = CallbackEmulator(self.sound_pressure_level.get_decibel,
                                            self.cb_decibel)
        self.cbe_decibel.set_period(100)

        self.show_device_information(device_information)

    def cb_decibel(self, decibel):
        if (100 < decibel < 600):
            self.cbe_decibel_below_60 = True
        if (600 < decibel < 1000):
            self.cbe_decibel_above_60 = True

        if self.cbe_decibel_below_60 and self.cbe_decibel_above_60:
            set_value = self.mw.set_value_okay
        else:
            set_value = self.mw.set_value_action

        set_value('Decibel: {0}dB(A)'.format(decibel/10.0))
