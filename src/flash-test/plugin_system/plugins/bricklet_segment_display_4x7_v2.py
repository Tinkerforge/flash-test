# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2019 Olaf Lüke <olaf@tinkerforge.com>

bricklet_segment_display_4x7_v2.py: Segment Display 4x7 2.0 plugin

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

from ..tinkerforge.bricklet_segment_display_4x7_v2 import BrickletSegmentDisplay4x7V2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
2. Verbinde Segment Display 4x7 2.0 Bricklet mit Port C
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Alle Elemente wechseln zwischen: Aus, an (dunkel), an (hell).
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_value = None
        self.state = 0

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

    def get_device_identifier(self):
        return BrickletSegmentDisplay4x7V2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletSegmentDisplay4x7V2.DEVICE_URL_PART))

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_value != None:
            self.cbe_value.set_period(0)

        self.sd4x7 = BrickletSegmentDisplay4x7V2(device_information.uid, self.get_ipcon())
        if self.sd4x7.get_bootloader_mode() != BrickletSegmentDisplay4x7V2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.cbe_value = CallbackEmulator(self.sd4x7.get_brightness,
                                          self.cb_value,
                                          ignore_last_data=True)

        self.cbe_value.set_period(500)

        self.show_device_information(device_information)


    def cb_value(self, _):
        if self.state == 0:
            self.sd4x7.set_segments([False]*8, [False]*8, [False]*8, [False]*8, [False]*2, False)
        elif self.state == 1:
            self.sd4x7.set_brightness(0)
            self.sd4x7.set_segments([True]*8, [True]*8, [True]*8, [True]*8, [True]*2, True)
        elif self.state == 2:
            self.sd4x7.set_brightness(7)
            self.sd4x7.set_segments([True]*8, [True]*8, [True]*8, [True]*8, [True]*2, True)

        self.state += 1
        if self.state > 2:
            self.state = 0
