# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Matthias Bolte <matthias@tinkerforge.com>

bricklet_segment_display_4x7.py: Segment Display 4x7 plugin

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

from ..tinkerforge.bricklet_segment_display_4x7 import BrickletSegmentDisplay4x7
from ..bricklet_base import BrickletBase, get_bricklet_firmware_filename

class Plugin(BrickletBase):
    TODO_TEXT = u"""\
2. Verbinde Segment Display 4x7 Bricklet mit Port C
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich wieder auf "Plugin gefunden")
5. Segment Display sollte hochzählen.
6. Das Bricklet ist fertig, in normale ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
7. Gehe zu 1
"""

    def __init__(self, *args):
        BrickletBase.__init__(self, *args)

    def start(self, device_information):
        BrickletBase.start(self, device_information)

        if device_information:
            self.new_enum(device_information)

    def stop(self):
        pass

    def get_device_identifier(self):
        return BrickletSegmentDisplay4x7.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename('segment_display_4x7'))

    def new_enum(self, device_information):
        self.sd4x7 = BrickletSegmentDisplay4x7(device_information.uid, self.get_ipcon())
        self.sd4x7.start_counter(1000, 9999, 1, 1)

        self.show_device_information(device_information)

        
