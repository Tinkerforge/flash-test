# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

brick_master.py: Master plugin

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

from ..tinkerforge.brick_master import BrickMaster
from ..tinkerforge.bricklet_joystick import BrickletJoystick
from ..brick_base import BrickBase, get_brick_firmware_filename
from ..callback_emulator import CallbackEmulator

LIMIT = 15

class Plugin(BrickBase):
    TODO_TEXT = u"""
1. Verbinde Master Brick mit PC per Mini-USB
2. Falls Brick nicht automatisch geflasht wird, drücke "Erase"- und "Reset"-Taster
3. Blaue LED neben Mini-USB buchse muss leuchten, 4 blaue LEDs an der Seite
   müssen einmal Lauflicht anzeigen
4. Gehe zu 1

* Weitere Tests (Stapel und Extension) findet im Brick Viewer statt
"""
    FIRMWARE_FILENAME = get_brick_firmware_filename(BrickMaster.DEVICE_URL_PART)
    qtcb_pressed0 = QtCore.pyqtSignal()
    qtcb_released0 = QtCore.pyqtSignal()
    qtcb_pressed1 = QtCore.pyqtSignal()
    qtcb_released1 = QtCore.pyqtSignal()
    qtcb_pressed2 = QtCore.pyqtSignal()
    qtcb_released2 = QtCore.pyqtSignal()
    qtcb_pressed3 = QtCore.pyqtSignal()
    qtcb_released3 = QtCore.pyqtSignal()

    def __init__(self, *args):
        BrickBase.__init__(self, *args)

        self.qtcb_pressed = [self.qtcb_pressed0, self.qtcb_pressed1, self.qtcb_pressed2, self.qtcb_pressed3]
        self.qtcb_released = [self.qtcb_released0, self.qtcb_released1, self.qtcb_released2, self.qtcb_released3]
        self.cbe_position = [None]*4
        self.position_transition = [[0, 0, 0, 0]]*4 # [TR, BR, BL, TL] 0 = not arrived, 1 = arrived, 2 = arrived and left
        self.button_transition = [0]*4 # 0 = not pressed, 1 = pressed, 2 = pressed and released
        self.last_position = [0, 0]*4
        self.last_position_status = ['?', '?', '?', '?']*4
        self.last_button_status = ['?']*4
        self.joystick_strings = ['']*4
        self.status = [False]*4

        self.qtcb_pressed[0].connect(lambda: self.cb_button(True, 0))
        self.qtcb_released[0].connect(lambda: self.cb_button(False, 0))
        self.qtcb_pressed[1].connect(lambda: self.cb_button(True, 1))
        self.qtcb_released[1].connect(lambda: self.cb_button(False, 1))
        self.qtcb_pressed[2].connect(lambda: self.cb_button(True, 2))
        self.qtcb_released[2].connect(lambda: self.cb_button(False, 2))
        self.qtcb_pressed[3].connect(lambda: self.cb_button(True, 3))
        self.qtcb_released[3].connect(lambda: self.cb_button(False, 3))

        self.joystick = [None]*4


    def start(self):
        BrickBase.start(self)

    def stop(self):
        for i in range(4):
            if self.cbe_position[i] != None:
                self.cbe_position[i].set_period(0)

    def get_device_identifier(self):
        return BrickMaster.DEVICE_IDENTIFIER

    def new_enum(self, device_information):
        def get_pos_lambda(i):
            return lambda x: self.cb_position(x, i)

        for i in range(4):
            if self.cbe_position[i] != None:
                self.cbe_position[i].set_period(0)

            self.joystick[i] = BrickletJoystick('Joy' + chr(ord('A') + i), self.get_ipcon())
            self.joystick[i].register_callback(self.joystick[i].CALLBACK_PRESSED, self.qtcb_pressed[i].emit)
            self.joystick[i].register_callback(self.joystick[i].CALLBACK_RELEASED, self.qtcb_released[i].emit)

            self.cbe_position[i] = CallbackEmulator(self.joystick[i].get_position, get_pos_lambda(i))
            self.cbe_position[i].set_period(100)

            if i == 0:
                self.show_device_information(device_information)

            self.position_transition[i] = [0, 0, 0, 0]
            self.button_transition[i] = 0
            self.last_position_status[i] = ['?', '?', '?', '?']
            self.last_button_status[i] = '?'
            self.last_position[i] = [0, 0]
            self.joystick_strings[i] = ''
            self.status[i] = False

            x, y = self.joystick[i].get_position()
            pressed = self.joystick[i].is_pressed()

            self.update_transition(x, y, pressed, i)

    def update_transition(self, x, y, pressed, port):
        if x != None and y != None:
            # TR
            if self.position_transition[port][0] == 0 and x >= LIMIT and y >= LIMIT:
                self.position_transition[port][0] = 1
            elif self.position_transition[port][0] == 1 and not (x >= LIMIT and y >= LIMIT):
                self.position_transition[port][0] = 2

            # BR
            if self.position_transition[port][1] == 0 and x >= LIMIT and y <= -LIMIT:
                self.position_transition[port][1] = 1
            elif self.position_transition[port][1] == 1 and not (x >= LIMIT and y <= -LIMIT):
                self.position_transition[port][1] = 2

            # BL
            if self.position_transition[port][2] == 0 and x <= -LIMIT and y <= -LIMIT:
                self.position_transition[port][2] = 1
            elif self.position_transition[port][2] == 1 and not (x <= -LIMIT and y <= -LIMIT):
                self.position_transition[port][2] = 2

            # TL
            if self.position_transition[port][3] == 0 and x <= -LIMIT and y >= LIMIT:
                self.position_transition[port][3] = 1
            elif self.position_transition[port][3] == 1 and not (x <= -LIMIT and y >= LIMIT):
                self.position_transition[port][3] = 2

        if pressed != None:
            if self.button_transition[port] == 0 and pressed:
                self.button_transition[port] = 1
            elif self.button_transition[port] == 1 and not pressed:
                self.button_transition[port] = 2

        if x != None and y != None:
            tr = '\u25C7'
            if x >= LIMIT and y >= LIMIT:
                tr = '\u25C6'

            br = '\u25C7'
            if x >= LIMIT and y <= -LIMIT:
                br = '\u25C6'

            bl = '\u25C7'
            if x <= -LIMIT and y <= -LIMIT:
                bl = '\u25C6'

            tl = '\u25C7'
            if x <= -LIMIT and y >= LIMIT:
                tl = '\u25C6'

            self.last_position_status[port] = [tr, br, bl, tl]
        else:
            tr, br, bl, tl = self.last_position_status[port]

        if pressed != None:
            bs = '\u25C7'
            if pressed:
                bs = '\u25C6'

            self.last_button_status[port] = bs
        else:
            bs = self.last_button_status[port]

        set_value = self.mw.set_value_action
        if self.position_transition[port] != [2, 2, 2, 2] or self.button_transition[port] != 2:
            status = 'Warte auf '

            for ps in self.position_transition[port]:
                if ps == 0:
                    status += '\u25C6 '
                elif ps == 1:
                    status += '\u25C7 '
                elif ps == 2:
                    status += '\u2611 '
                else:
                    status += '? '

            status += 'und '

            if self.button_transition[port] == 0:
                status += '\u25C6'
            elif self.button_transition[port] == 1:
                status += '\u25C7'
            elif self.button_transition[port] == 2:
                status += '\u2611'
            else:
                status += str(self.button_transition[port])
        else:
            status = 'Test OK!'
            self.status[port] = True
        
        if self.status == [True]*4:
            set_value = self.mw.set_value_okay

        if x != None and y != None:
            self.last_position[port] = [x, y]
        else:
            x, y = self.last_position[port]

        self.joystick_strings[port] = " Position: ({0}, {1})\n Ecken und Taster: {2} {3} {4} {5} und {6}, {7} (\u25C6 = drin/gedrückt, \u25C7 = draußen/losgelassen, \u2611 = OK)".format(x, y, tr, br, bl, tl, bs, status)
        set_value('Joystick A:\n' + self.joystick_strings[0] + '\nJoystick B:\n' + self.joystick_strings[1] + '\nJoystick C:\n' + self.joystick_strings[2] + '\nJoystick D:\n' + self.joystick_strings[3])

    def cb_position(self, data, port):
        x, y = data
        self.update_transition(x, y, None, port)

    def cb_button(self, pressed, port):
        self.update_transition(None, None, pressed, port)