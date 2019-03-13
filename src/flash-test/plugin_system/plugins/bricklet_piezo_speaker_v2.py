# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_piezo_speaker_v2.py: Piezo Speaker 2.0 plugin

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

from ..tinkerforge.bricklet_piezo_speaker_v2 import BrickletPiezoSpeakerV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Verbinde Piezo Speaker Bricklet 2.0 mit Port C
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Überprüfe: Es wird eine aufsteigende Tonfolge abgespielt, Lautstärke ändert sich
5. Das Bricklet ist fertig, zuschweißen, Aufkleber aufkleben
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_value = None
        self.volume = 0

    def start(self, device_information):
        CoMCUBrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletPiezoSpeakerV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletPiezoSpeakerV2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)

        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.piezo_speaker = BrickletPiezoSpeakerV2(device_information.uid, self.get_ipcon())
        if self.piezo_speaker.get_bootloader_mode() != BrickletPiezoSpeakerV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_value = CallbackEmulator(self.piezo_speaker.get_alarm, self.cb_value)
        self.cbe_value.set_period(100)

        self.show_device_information(device_information)

        self.piezo_speaker.set_alarm(250, 750, 1, 5, 0, 10000)

    def cb_value(self, _):
        self.volume += 1
        if self.volume > 10:
            self.volume = 0

        self.piezo_speaker.update_volume(self.volume)
