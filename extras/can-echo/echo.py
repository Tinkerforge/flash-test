#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "5551"

from ip_connection import IPConnection
from bricklet_can import BrickletCAN

# Callback function for frame read callback
def cb_frame_read(can, frame_type, identifier, data, length):
    can.write_frame(frame_type, identifier, data, length)

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    can = BrickletCAN(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register frame read callback to function cb_frame_read
    can.register_callback(can.CALLBACK_FRAME_READ, lambda *args: cb_frame_read(can, *args))

    # Enable frame read callback
    can.enable_frame_read_callback()

    raw_input("Press key to exit\n") # Use input() in Python 3
    can.disable_frame_read_callback()
    ipcon.disconnect()
