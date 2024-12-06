# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2024 Olaf Lüke <olaf@tinkerforge.com>

bricklet_warp_energy_manager_v2.py: WARP Energy Manager 2.0 plugin

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

from ..tinkerforge.bricklet_warp_energy_manager_v2 import BrickletWARPEnergyManagerV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. Lege WARP Energy Manager 2.0 in Testkiste, verbinde alle Stecker, stecke SD-Karte ein
2. Schließe Testkiste
3. Drücke "Flashen"
4. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
5. Warte bis alles getestet ist (IO, SD, Zähler)
6. Das Bricklet ist fertig
7. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.cbe_input = None

    def start(self):
        CoMCUBrickletBase.start(self)

    def stop(self):
        super().stop()
        if self.cbe_input != None:
            self.cbe_input.set_period(0)

    def get_device_identifier(self):
        return BrickletWARPEnergyManagerV2.DEVICE_IDENTIFIER

    def flash_clicked(self):
        self.flash_bricklet(get_bricklet_firmware_filename(BrickletWARPEnergyManagerV2.DEVICE_URL_PART), power_off_duration=10, try_count=1000)

    def new_enum(self, device_information):
        CoMCUBrickletBase.new_enum(self, device_information)
        if self.cbe_input != None:
            self.cbe_input.set_period(0)

        self.wem = BrickletWARPEnergyManagerV2(device_information.uid, self.get_ipcon())
        if self.wem.get_bootloader_mode() != BrickletWARPEnergyManagerV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.io0_ok     = False
        self.io1_ok     = False
        self.io2_ok     = False
        self.io3_ok     = False
        self.voltage_ok = False
        self.sd_ok      = False
        self.meter_ok   = False
        self.counter    = 0

        self.cbe_input = CallbackEmulator(self.wem.get_input, self.cb_get_input, ignore_last_data=True)
        self.cbe_input.set_period(250)

        self.show_device_information(device_information)

    def cb_get_input(self, value):
        if self.counter == 0:
            self.wem.set_sg_ready_output(0, 0)
            self.wem.set_sg_ready_output(1, 0)
            self.wem.set_relay_output(0, 0)
            self.wem.set_relay_output(1, 0)
            self.mw.set_tool_status_normal("Prüfe IO 0 0 0 0")
            self.counter += 1
        elif self.counter == 1:
            if value != (False, False, False, False):
                self.mw.set_value_error("IO hat nicht reagiert")
                return
            else:
                self.counter += 1
        elif self.counter == 2:
            self.wem.set_sg_ready_output(0, 1)
            self.wem.set_sg_ready_output(1, 0)
            self.wem.set_relay_output(0, 0)
            self.wem.set_relay_output(1, 0)
            self.mw.set_tool_status_normal("Prüfe IO 1 0 0 0")
            self.counter += 1
        elif self.counter == 3:
            if value != (True, False, False, False):
                self.mw.set_value_error("SG ready 0 oder input 0 hat nicht reagiert")
                return
            else:
                self.io0_ok = True
                self.counter += 1
        elif self.counter == 4:
            self.wem.set_sg_ready_output(0, 0)
            self.wem.set_sg_ready_output(1, 1)
            self.wem.set_relay_output(0, 0)
            self.wem.set_relay_output(1, 0)
            self.mw.set_tool_status_normal("Prüfe IO 0 1 0 0")
            self.counter += 1
        elif self.counter == 5:
            if value != (False, True, False, False):
                self.mw.set_value_error("SG ready 1 oder input 1 hat nicht reagiert")
                return
            else:
                self.io1_ok = True
                self.counter += 1
        elif self.counter == 6:
            self.wem.set_sg_ready_output(0, 0)
            self.wem.set_sg_ready_output(1, 0)
            self.wem.set_relay_output(0, 1)
            self.wem.set_relay_output(1, 0)
            self.mw.set_tool_status_normal("Prüfe IO 0 0 1 0")
            self.counter += 1
        elif self.counter == 7:
            if value != (False, False, True, False):
                self.mw.set_value_error("Relay 0 oder input 2 hat nicht reagiert")
                return
            else:
                self.io2_ok = True
                self.counter += 1
        elif self.counter == 8:
            self.wem.set_sg_ready_output(0, 0)
            self.wem.set_sg_ready_output(1, 0)
            self.wem.set_relay_output(0, 0)
            self.wem.set_relay_output(1, 1)
            self.mw.set_tool_status_normal("Prüfe IO 0 0 0 1")
            self.counter += 1
        elif self.counter == 9:
            if value != (False, False, False, True):
                self.mw.set_value_error("Relay 1 oder input 3 hat nicht reagiert")
                return
            else:
                self.io3_ok = True
                self.counter += 1
        elif self.counter == 10:
            self.wem.format_sd(0x4223ABCD)
            self.mw.set_tool_status_normal("Formatiere SD-Karte")
            self.counter += 1
        elif self.counter == 11:
            self.mw.set_tool_status_normal("Prüfe Spannung")
            voltage = self.wem.get_input_voltage()
            if 11500 < voltage < 12500:
                self.voltage_ok = True
                self.counter += 1
            else:
                self.mw.set_value_error("Unerwartete Spannung: {0} mV".format(voltage))
        elif self.counter < 39:
            self.mw.set_tool_status_normal("Prüfe SD-Karte")
            self.counter += 1
            sd_info = self.wem.get_sd_information()
            if (sd_info.sd_status) == 0 and (sd_info.lfs_status) == 0:
                self.sd_ok = True
                self.counter = 40
        elif self.counter == 40:
            state = self.wem.get_energy_meter_state()
            if state.energy_meter_type == self.wem.ENERGY_METER_TYPE_DSZ15DZMOD:
                self.meter_ok = True
            else:
                self.mw.set_tool_status_normal("Prüfe Zähler")

        set_value = self.mw.set_value_action
        if self.io0_ok and self.io1_ok and self.io2_ok and self.io3_ok and self.voltage_ok and self.sd_ok and self.meter_ok:
            set_value = self.mw.set_value_okay
            self.mw.set_tool_status_normal("Alles OK. Fertig.")

        set_value("IO: {0} {1} {2} {3}  Spannung {4}  SD: {5}  Zähler: {6}".format(
            '\u2611' if self.io0_ok     else "-",
            '\u2611' if self.io1_ok     else "-",
            '\u2611' if self.io2_ok     else "-",
            '\u2611' if self.io3_ok     else "-",
            '\u2611' if self.voltage_ok else "-",
            '\u2611' if self.sd_ok      else "-",
            '\u2611' if self.meter_ok   else "-")
        )