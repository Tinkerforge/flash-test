#!/bin/sh

# store this file in /home/tf and add @/home/tf/red-brick-test.sh to
# /home/tf/.config/lxsession/LXDE/autostart

DISPLAY=:0 lxterminal -e "watch -n 0.5 /home/tf/red-brick-test.py"
