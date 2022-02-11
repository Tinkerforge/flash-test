# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

extension_ethernet_wo_poe.py: Ethernet Extension w/o PoE plugin

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

from .extension_ethernet import Plugin as ExtensionEthernetPlugin

class Plugin(ExtensionEthernetPlugin):
    TODO_TEXT = u"""\
1. Verbinde Ethernet-Kabel mit Ethernet Extension
2. Stecke Ethernet Extension auf Master Brick
3. Starte Master Brick neu
4. Warte bis Ethernet gefunden wird
5. Trage MAC Adresse ein und drücke Knopf "MAC Adresse schreiben"
6. Warte bis Ethernet-Verbindung hergestellt wird
7. MAC Adressen-Aufkleber aufkleben
8. Die Extension ist fertig, in ESD-Tüte stecken, zuschweißen, Aufkleber aufkleben
9. Gehe zu 1
"""

    def get_device_identifier(self):
        return 35 # without PoE
