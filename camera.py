#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  camera.py
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

from math_3d import Vec3
from another_thing import Thing


class Camera(Thing):
    """ El "camera" está definido por:
            loc         Ubicacion
            look_at     Direccion
            up          Orientacion
            angle       Angulo de apertura
    """
    def __init__(self, tkns):
        super().__init__(tkns)
        if not 'angle' in self.params:      # 'angle' has default value 66
            self.params['angle'] = 66


def test_camera():
    cam = Camera(['location', Vec3(1, 2, 3), 'look_at', Vec3(4, 5, 6),
                  'up', Vec3(7, 8, 9), 'angle', 55])
    print(cam)


def main(args):
    test_camera()



if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))



