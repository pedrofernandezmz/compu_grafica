#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  extract.py
#
#  Copyright 2023 John Coppens <john@jcoppens.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

class Vec3:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z


class Thing:
    # pars is a 1D list of key/value pairs. The constructor converts them to
    # a dictionary
    def __init__(self, pars = []):
        self.params = {pars[x]: pars[x+1] for x in range(0, len(pars), 2)}


class Camera(Thing):
    def __init__(self, tkns):
        super().__init__(tkns)
        if not 'angle' in self.params:      # 'angle' has default value 66
            self.params['angle'] = 66

SCENE = [
['#include', "colors.inc"],
['#include', "woods.inc"],
['camera', 'loc',     Vec3(0, 3, 0),
           'look_at', Vec3(5, 0, 0),
           'up',      Vec3(0, 1, 0),
           'angle',   60]
]


def main(args):
    catalog = {
        'cameras': [],
        'lights':  [],
        'things':  []
    }

    for el in SCENE:
        key = el[0]
        if key.startswith('#'):             # Is a directive?
            continue

        elif key == 'camera':
            # ~ catalog['cameras'].append(Camera(el[1:]))
            catalog['cameras'].append(Camera(['loc', Vec3(1, 2, 3),
                                              'look_at', Vec3(4, 5, 6),
                                              'up', Vec3(7, 8, 9),
                                              'angle', 55]))

        else:
            print('Panic...')
            exit(1)

    print(catalog)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
