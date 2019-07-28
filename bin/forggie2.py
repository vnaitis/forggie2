#!/usr/bin/env python
"""Script to start the game.

A game inspired by Frogger.

Copyright (c) 2019 V. Naitis.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""
import os
import sys

currentDir = os.path.dirname(os.path.abspath(__file__))
srcPath = os.path.join(currentDir, '..', 'forggie2')
sys.path.insert(0, srcPath)
import main

main.main()
