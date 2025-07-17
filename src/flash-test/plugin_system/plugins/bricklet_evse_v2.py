# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2021 Olaf Lüke <olaf@tinkerforge.com>

bricklet_evse_v2.py: EVSE 2.0 plugin

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

from PyQt5 import Qt, QtGui, QtCore, QtWidgets

from ..tinkerforge.bricklet_evse_v2 import BrickletEVSEV2
from ..comcu_bricklet_base import CoMCUBrickletBase, get_bricklet_firmware_filename
from ..callback_emulator import CallbackEmulator

import time
import subprocess
import os
import traceback

from ..evse_v3_tester import EVSEV3Tester

class Plugin(CoMCUBrickletBase):
    TODO_TEXT = u"""\
1. EVSE 3.0 Bricklet an EVSE-Tester anschließen
2. Drücke "Flashen"
3. Warte bis Master Brick neugestartet hat (Tool Status ändert sich auf "Plugin gefunden")
4. Drücke "Test Neustarten" um Test zu starten
5. Das Bricklet ist fertig
6. Gehe zu 1
"""

    def __init__(self, *args):
        CoMCUBrickletBase.__init__(self, *args)
        self.after_flash_clicked = False
        self.test_running = False
        self.evse_tester = None
        self.auto_flash_locked = False
        self.auto_flash_requested = False
        self.auto_flash_timer = QtCore.QTimer(self)
        self.auto_flash_timer.timeout.connect(self.cb_check_auto_flash)
        self.enum_count = 0

    def start(self):
        CoMCUBrickletBase.start(self)
        l = self.mw.evse_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(True)

        self.evse_tester = EVSEV3Tester(log_func=no_log, start_func=self.request_auto_flash)
        self.evse_tester.setup()

        self.auto_flash_locked = False
        self.auto_flash_requested = False
        self.auto_flash_timer.start(500)

    def stop(self):
        CoMCUBrickletBase.stop(self)
        l = self.mw.evse_layout
        for i in range(l.count()):
            l.itemAt(i).widget().setVisible(False)

        self.auto_flash_timer.stop()

    def get_device_identifier(self):
        return BrickletEVSEV2.DEVICE_IDENTIFIER

    def request_auto_flash(self):
        if not self.auto_flash_locked:
            self.auto_flash_requested = True

    def cb_check_auto_flash(self):
        if self.auto_flash_requested:
            self.auto_flash_locked = True
            self.auto_flash_requested = False
            QtCore.QTimer.singleShot(500, self.flash_clicked)

    def flash_clicked(self):
        self.mw.evse_textedit.clear()
        self.evse_tester.set_led(0, 0, 255)

        if not self.flash_bricklet(get_bricklet_firmware_filename(BrickletEVSEV2.DEVICE_URL_PART), 0.5):
            self.evse_tester.set_led(255, 0, 0)
            self.auto_flash_locked = False
        else:
            self.after_flash_clicked = True

    def new_enum(self, device_information):
        self.enum_count += 1
        CoMCUBrickletBase.new_enum(self, device_information)

        self.evse = BrickletEVSEV2(device_information.uid, self.get_ipcon())
        if self.evse.get_bootloader_mode() != BrickletEVSEV2.BOOTLOADER_MODE_FIRMWARE:
            return

        self.show_device_information(device_information)
        if self.after_flash_clicked:
            self.after_flash_clicked = False
            self.restart_button_clicked()

    def restart_button_clicked(self):
        self.start_test(True, True, False)

    def start_test(self, retry_allowed, clear_textedit, is_retry):
        if self.test_running:
            return

        retry = False

        try:
            self.test_running = True

            if clear_textedit:
                self.mw.evse_textedit.clear()
                QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 50)

            test_iterator = evse_v3_test_generator(self.evse_tester)

            for i in test_iterator:
                if i is not None:
                    self.mw.evse_textedit.append(i)
                QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 50)

            if is_retry:
                self.mw.evse_textedit.append('Dies ware der zweite Versuch!')
                QtWidgets.QApplication.processEvents(QtCore.QEventLoop.AllEvents, 50)
        except:
            self.mw.evse_textedit.append('-----------------> Fehler im Testablauf:\n' + traceback.format_exc() + '\n')

            if retry_allowed:
                retry = True
            else:
                try:
                    evse_tester.exit(1)
                except:
                    pass
        finally:
            self.test_running = False

        if retry:
            self.start_test(False, False, True)
        else:
            self.auto_flash_locked = False

TEST_LOG_FILENAME = "full_test_log.csv"
TEST_LOG_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', '..', '..', '..', 'wallbox', 'evse_v3_test_report'))

def test_log_pull():
    try:
        inp = ['git', 'pull']
        out = subprocess.check_output(inp , stderr=subprocess.STDOUT, encoding='utf-8', cwd=TEST_LOG_DIRECTORY)
        ret = '   -> {}'.format(' '.join(inp))
        ret += '\n      {}'.format(out)
        return 0, ret
    except subprocess.CalledProcessError as e:
        ret = 'Error: git pull failed:\n' + e.output.strip()
        return 1, ret
    except Exception as e:
        ret = 'Error: git pull failed:\n' + str(e)
        return 1, ret

def test_log_commit_and_push(uid):
    commit_message = 'Add test report for EVSE Bricklet 3.0 with UID ' + uid
    test_log_pull()

    try:
        inp = ['git', 'commit', TEST_LOG_FILENAME, '-m', commit_message]
        out = subprocess.check_output(inp, stderr=subprocess.STDOUT, encoding='utf-8', cwd=TEST_LOG_DIRECTORY)
        ret = '   -> {}'.format(' '.join(inp))
        ret += '\n      {}'.format(out)
    except subprocess.CalledProcessError as e:
        ret = 'Error: git commit failed:\n' + e.output.strip()
        return 1, ret
    except Exception as e:
        ret = 'Error: git commit failed:\n' + str(e)
        return 1, ret

    try:
        inp = ['git', 'push']
        out = subprocess.check_output(inp, stderr=subprocess.STDOUT, encoding='utf-8', cwd=TEST_LOG_DIRECTORY)
        ret += '\n   -> {}'.format(' '.join(inp))
        ret += '\n      {}'.format(out)
        return 0, ret
    except subprocess.CalledProcessError as e:
        ret = 'Error: git push failed:\n' + e.output.strip()
        return 1, ret
    except Exception as e:
        ret = 'Error: git push failed:\n' + str(e)
        return 1, ret

def no_log(s):
    pass

def test_value(value, expected, margin_percent=0.1, margin_absolute=20):
    if value < 0 and expected > 0:
        return False
    if value > 0 and expected < 0:
        return False

    value = abs(value)
    expected = abs(expected)

    return (value*(1-margin_percent) - margin_absolute) < expected < (value*(1+margin_percent) + margin_absolute)

def evse_v3_test_generator(evse_tester, mw):
    yield('Schaltereinstellung auf 32A stellen (1=Off, 2=Off, 3=On, 4=On) !!!')

    yield('Suche EVSE Bricklet 3.0 und Tester')
    evse_tester.setup()
    evse_tester.set_led(0, 0, 255)

    if evse_tester.find_evse():
        yield('... OK')
    else:
        yield("Konnte EVSE Bricklet 3.0 nicht finden.")
        evse_tester.exit(1)
        return

    yield("Aktualisiere Testreports...")

    ok, s = test_log_pull()
    yield(s)
    if ok != 0:
        yield("Konnte wallbox git nicht finden.")
        yield("Wallbox git wird benötigt um den Testbericht zu speichern.")
        evse_tester.exit(1)
        return
    yield('... OK')

    yield('Prüfe Hardware-Version (erwarte 3.0)')
    hv = evse_tester.get_hardware_version()
    if hv == 30:
        yield('... OK')
    else:
        yield('-----------------> NICHT OK: {0}'.format(hv))
        evse_tester.exit(1)
        return

    data = []

    ident = evse_tester.evse.get_identity()
    data.append(ident.uid)

    # Initial config
    evse_tester.set_contactor_fb(False)
    evse_tester.set_230v(True)
    evse_tester.set_cp_pe_resistor(False, False, False)
    evse_tester.set_pp_pe_resistor(False, False, True, False)

    start = time.time()
    count = mw.enum_count
    yield('Reset EVSE Bricklet')
    evse_tester.evse.reset()
    while mw.enum_count != (count + 1):
        if (time.time() - start) > 10:
            yield('-----------------> NICHT OK: EVSE Bricklet hat nicht neu enumeriert')
            evse_tester.exit(1)
            return
        time.sleep(0.1)
        yield(None)
    yield('... OK ({0:.1f} Sekunden)'.format(time.time() - start))

    yield('Warte auf DC-Schutz Kalibrierung (1.5 Sekunden)')
    time.sleep(1.2)
    yield('... OK')

    start = time.time()
    while True:
        if time.time() - start > 2:
            yield('-----------------> NICHT OK: Konnte Hardware-Konfiguration nicht abfragen')
            evse_tester.exit(1)
            return
        try:
            hw_conf = evse_tester.evse.get_hardware_configuration()
        except:
            time.sleep(0.1)
            yield(None)
            continue
        break

    yield('Teste Schalter-Einstellung')
    if hw_conf.jumper_configuration != 6:
        yield('Falsche Schalter-Einstellung: {0}'.format(hw_conf.jumper_configuration))
        yield('-----------------> NICHT OK')
        evse_tester.exit(1)
        return
    else:
        yield('... OK')

    yield('Teste Lock-Switch-Einstellung')
    if hw_conf.has_lock_switch:
        yield('Falsche Lock-Switch-Einstellung: {0}'.format(hw_conf.has_lock_switch))
        yield('-----------------> NICHT OK')
        evse_tester.exit(1)
        return
    else:
        yield('... OK')

    yield('Teste Shutdown Input high')
    evse_tester.shutdown_input_enable(True)
    time.sleep(0.1)
    value = evse_tester.evse.get_low_level_state().gpio[18]
    if value:
        yield('-----------------> NICHT OK')
        evse_tester.exit(1)
        return
    else:
        yield('... OK')

    yield('Teste Shutdown Input low')
    evse_tester.shutdown_input_enable(False)
    time.sleep(0.1)
    value = evse_tester.evse.get_low_level_state().gpio[18]
    if not value:
        yield('-----------------> NICHT OK')
        evse_tester.exit(1)
        return
    else:
        yield('... OK')

    yield('Teste CP/PE...')
    yield(' * open')
    evse_tester.set_max_charging_current(0)
    while True:
        res_cppe = evse_tester.evse.get_low_level_state().resistances[0]
        if res_cppe == 4294967295:
            yield(' * ... OK ({0} Ohm)'.format(res_cppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 4294967295 Ohm)'.format(res_cppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)
        yield(None)
    vol_cppe = evse_tester.get_cp_pe_voltage()
    if test_value(vol_cppe, 12213):
        yield(' * ... OK ({0} mV)'.format(vol_cppe))
    else:
        yield('-----------------> NICHT OK {0} mV (erwartet 12213 mV)'.format(vol_cppe))
        evse_tester.exit(1)
        return

    yield(' * 2700 Ohm')
    evse_tester.set_cp_pe_resistor(True, False, False)

    start = time.time()
    while True:
        time.sleep(0.1)
        res_cppe = evse_tester.evse.get_low_level_state().resistances[0]
        data.append(str(res_cppe))
        if test_value(res_cppe, 2700):
            yield(' * ... OK ({0} Ohm)'.format(res_cppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 2700 Ohm)'.format(res_cppe))
                evse_tester.exit(1)
                return
    while True:
        vol_cppe = evse_tester.get_cp_pe_voltage()
        if test_value(vol_cppe, 9069):
            yield(' * ... OK ({0} mV)'.format(vol_cppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} mV (erwartet 9069 mV)'.format(vol_cppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)

    yield(' * 880 Ohm')
    evse_tester.set_cp_pe_resistor(True, True, False)

    start = time.time()
    while True:
        time.sleep(0.1)
        res_cppe = evse_tester.evse.get_low_level_state().resistances[0]
        data.append(str(res_cppe))
        if test_value(res_cppe, 880):
            yield(' * ... OK ({0} Ohm)'.format(res_cppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 880 Ohm)'.format(res_cppe))
                evse_tester.exit(1)
                return
    while True:
        vol_cppe = evse_tester.get_cp_pe_voltage()
        if test_value(vol_cppe, 6049):
            yield(' * ... OK ({0} mV)'.format(vol_cppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} mv (erwartet 6049 mV)'.format(vol_cppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)

    yield(' * 240 Ohm')
    evse_tester.set_cp_pe_resistor(True, False, True)

    start = time.time()
    while True:
        time.sleep(0.1)
        res_cppe = evse_tester.evse.get_low_level_state().resistances[0]
        data.append(str(res_cppe))
        if test_value(res_cppe, 240):
            yield(' * ... OK ({0} Ohm)'.format(res_cppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 240 Ohm)'.format(res_cppe))
                evse_tester.exit(1)
                return

    while True:
        vol_cppe = evse_tester.get_cp_pe_voltage()
        if test_value(vol_cppe, 3039):
            yield(' * ... OK ({0} mV)'.format(vol_cppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} mV (erwartet 2646 mV)'.format(vol_cppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)

    evse_tester.set_cp_pe_resistor(False, False, False)

    yield('Teste PP/PE...')
    yield(' * 220 Ohm')
    start = time.time()
    while True:
        time.sleep(0.1)
        res_pppe = evse_tester.evse.get_low_level_state().resistances[1]
        data.append(str(res_pppe))
        if test_value(res_pppe, 220):
            yield(' * ... OK ({0} Ohm)'.format(res_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 220 Ohm)'.format(res_pppe))
                evse_tester.exit(1)
                return
    while True:
        vol_pppe = evse_tester.get_pp_pe_voltage()
        if test_value(vol_pppe, 834):
            yield(' * ... OK ({0} mV)'.format(vol_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} mv (erwartet 834 mV)'.format(vol_pppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)

    yield(' * 1500 Ohm')
    evse_tester.set_pp_pe_resistor(True, False, False, False)

    start = time.time()
    while True:
        time.sleep(0.1)
        res_pppe = evse_tester.evse.get_low_level_state().resistances[1]
        data.append(str(res_pppe))
        if test_value(res_pppe, 1500):
            yield(' * ... OK ({0} Ohm)'.format(res_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 1500 Ohm)'.format(res_pppe))
                evse_tester.exit(1)
                return
    while True:
        vol_pppe = evse_tester.get_pp_pe_voltage()
        if test_value(vol_pppe, 2313):
            yield(' * ... OK ({0} mV)'.format(vol_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} mv (erwartet 2313 mV)'.format(vol_pppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)

    yield(' * 680 Ohm')
    evse_tester.set_pp_pe_resistor(False, True, False, False)

    start = time.time()
    while True:
        time.sleep(0.1)
        res_pppe = evse_tester.evse.get_low_level_state().resistances[1]
        data.append(str(res_pppe))
        if test_value(res_pppe, 680):
            yield(' * ... OK ({0} Ohm)'.format(res_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 680 Ohm)'.format(res_pppe))
                evse_tester.exit(1)
                return
    while True:
        vol_pppe = evse_tester.get_pp_pe_voltage()
        if test_value(vol_pppe, 1695):
            yield(' * ... OK ({0} mV)'.format(vol_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} mV (erwartet 1695 mV)'.format(vol_pppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)

    yield(' * 100 Ohm')
    evse_tester.set_pp_pe_resistor(False, False, False, True)

    start = time.time()
    while True:
        time.sleep(0.1)
        res_pppe = evse_tester.evse.get_low_level_state().resistances[1]
        data.append(str(res_pppe))
        if test_value(res_pppe, 100):
            yield(' * ... OK ({0} Ohm)'.format(res_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} Ohm (erwartet 100 Ohm)'.format(res_pppe))
                evse_tester.exit(1)
                return
    while True:
        vol_pppe = evse_tester.get_pp_pe_voltage()
        if test_value(vol_pppe, 441):
            yield(' * ... OK ({0} mV)'.format(vol_pppe))
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK {0} mV (erwartet 441 mV)'.format(vol_pppe))
                evse_tester.exit(1)
                return
        time.sleep(0.1)

    evse_tester.set_pp_pe_resistor(False, False, True, False)
    time.sleep(0.5)

    yield('Beginne Test-Ladung')

    evse_tester.set_contactor_fb(False)
    evse_tester.set_230v(True)
    evse_tester.set_cp_pe_resistor(False, False, False)
    evse_tester.set_pp_pe_resistor(False, False, True, False)

    yield('Reset EVSE Bricklet')
    start = time.time()
    count = mw.enum_count
    evse_tester.evse.reset()
    while mw.enum_count != (count+1):
        if (time.time() - start) > 10:
            yield('-----------------> NICHT OK: EVSE Bricklet hat nicht neu enumeriert')
            evse_tester.exit(1)
            return
        time.sleep(0.1)
        yield(None)
    yield('... OK ({0:.1f} Sekunden)'.format(time.time() - start))


    yield('Warte auf DC-Schutz Kalibrierung (1.5 Sekunden)')
    for i in range(15):
        time.sleep(0.1)
        yield(None)
    yield('... OK')

    yield('Setze 2700 Ohm Widerstand')
    evse_tester.set_cp_pe_resistor(True, False, False)
    yield('... OK')
    time.sleep(0.1)

    yield('Setze 2700 Ohm + 1300 Ohm Widerstand')
    evse_tester.set_cp_pe_resistor(True, True, False)
    yield('... OK')

    yield('Aktiviere Schütz')
    if evse_tester.wait_for_contactor_gpio(False):
        yield('... OK')
    else:
        yield('-----------------> NICHT OK')
        evse_tester.exit(1)
        return

    yield('Aktiviere Schütz Test')
    evse_tester.set_contactor_fb(True)

    time.sleep(0.5)
    yield('... OK')

    test_voltages = [-10302, -9698, -9095, -8476, -7871, -7272, -6648, -6047, -5445, -4822, -4224, -3617, -3000, -2396]
    for i, a in enumerate(range(6, 33, 2)):
        yield('Test CP/PE {0}A'.format(a))
        evse_tester.set_max_charging_current(a*1000)
        start = time.time()
        res_cppe_ok = False
        vol_cppe_ok = False
        while not (res_cppe_ok and vol_cppe_ok):
            if not res_cppe_ok:
                res_cppe = evse_tester.evse.get_low_level_state().resistances[0]
                data.append(str(res_cppe))
                if test_value(res_cppe, 880):
                    yield(' * ... OK ({0} Ohm)'.format(res_cppe))
                    res_cppe_ok = True
                else:
                    if time.time() - start > 5:
                        yield('-----------------> NICHT OK {0} Ohm (erwartet 880 Ohm)'.format(res_cppe))
                        evse_tester.exit(1)
                        return
            if not vol_cppe_ok:
                vol_cppe = evse_tester.get_cp_pe_voltage()
                if test_value(vol_cppe, test_voltages[i], margin_percent=0.15):
                    yield(' * ... OK ({0} mV)'.format(vol_cppe))
                    vol_cppe_ok = True
                else:
                    if time.time() - start > 5:
                        yield('-----------------> NICHT OK {0} mV (erwartet {1} mV) -> Wahrscheinlich kein PWM'.format(vol_cppe, test_voltages[i]))
                        evse_tester.exit(1)
                        return
            time.sleep(0.1)

    yield('Teste Stromzähler')
    values, detailed_values, hw, error = evse_tester.get_energy_meter_data()
    if (not hw.energy_meter_type > 0) or (not values.phases_connected[0]):
        yield('-----------------> NICHT OK: {0}, {1}, {2}'.format(str(hw), str(error), str(values)))
        evse_tester.exit(1)
        return
    else:
        yield('... OK: {0}, {1}'.format(hw.energy_meter_type, values.phases_connected[0]))

    yield('Ausschaltzeit messen')
    t1 = time.time()
    evse_tester.set_cp_pe_resistor(True, False, False)
    if not evse_tester.wait_for_contactor_gpio(True):
        yield('-----------------> NICHT OK: Schütz hat nicht geschaltet')
        evse_tester.exit(1)
        return
    evse_tester.set_contactor_fb(False)
    t2 = time.time()

    delay = int((t2-t1)*1000)
    data.append(str(delay))
    yield('... OK')

    if delay <= 100:
        yield('Ausschaltzeit: {0}ms OK'.format(delay))
    else:
        yield('Ausschaltzeit: {0}ms'.format(delay))
        yield('-----------------> NICHT OK')
        evse_tester.exit(1)
        return

    yield('Teste Front-Taster')
    evse_tester.press_button(True)

    if evse_tester.wait_for_button_gpio(True): # Button True = Pressed
        yield('... OK')
    else:
        yield('-----------------> NICHT OK')
        evse_tester.exit(1)
        return
    evse_tester.press_button(False)

    yield('Teste LED R')
    evse_tester.set_evse_led(True, False, False)

    start = time.time()
    while True:
        time.sleep(0.1)
        led = evse_tester.get_evse_led()
        if led[0] and (not led[1]) and (not led[2]):
            yield('... OK')
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK: {0} {1} {2}'.format(*led))
                evse_tester.exit(1)
                return

    yield('Teste LED G')
    evse_tester.set_evse_led(False, True, False)

    start = time.time()
    while True:
        time.sleep(0.1)
        led = evse_tester.get_evse_led()
        if led[1] and (not led[0]) and (not led[2]):
            yield('... OK')
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK: {0} {1} {2}'.format(*led))
                evse_tester.exit(1)
                return

    yield('Teste LED B')
    evse_tester.set_evse_led(False, False, True)

    start = time.time()
    while True:
        time.sleep(0.1)
        led = evse_tester.get_evse_led()
        if led[2] and (not led[0]) and (not led[1]):
            yield('... OK')
            break
        else:
            if time.time() - start > 5:
                yield('-----------------> NICHT OK: {0} {1} {2}'.format(*led))
                evse_tester.exit(1)
                return

    yield("Speichere Testreport...")
    with open(os.path.join(TEST_LOG_DIRECTORY, TEST_LOG_FILENAME), 'a+') as f:
        f.write(', '.join(data) + '\n')

    ok, s = test_log_commit_and_push(ident.uid)
    yield(s)
    if ok == 0:
        yield('')
        yield('Fertig. Alles OK')

    evse_tester.exit(0)
    return
