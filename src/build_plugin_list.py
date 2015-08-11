#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
flash-test (Brick/Bricklet/Extension Flash and Test tool)
Copyright (C) 2015 Olaf Lüke <olaf@tinkerforge.com>

build_plugin_list.py: Generate list of plugins

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


import os
import sys

released_only = False

if len(sys.argv) > 1:
    if sys.argv[1] == 'release':
        released_only = True
    else:
        raise Exception('Unexpected argument ' + sys.argv[1])

imports = []
device_classes = []
root = os.path.abspath(__file__).replace(__file__, '')
plugin_system_dir = os.path.join(root, 'flash-test', 'plugin_system')
plugins_dir = os.path.join(plugin_system_dir, 'plugins')

for plugin in sorted(os.listdir(plugins_dir)):
    # Ignore __init__.py and folders
    if (not os.path.isfile(os.path.join(plugins_dir, plugin))) or (not plugin.endswith('py')) or '__init__.py' in plugin:
        continue

    plugin = plugin.replace('.py', '')

    imports.append('from .plugins.{0} import Plugin as {1}\n'.format(plugin, plugin + '_class'))
    device_classes.append('    {0},\n'.format(plugin + '_class'))

with open(os.path.join(plugin_system_dir, 'device_classes.py'), 'wb') as f:
    f.writelines(map(lambda s: s.encode('utf-8'), imports))
    f.write(b'\n')
    f.write(b'device_classes = [\n')
    f.writelines(map(lambda s: s.encode('utf-8'), device_classes))
    f.write(b']\n')
