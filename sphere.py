#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  modeller.py
#
#  Copyright 2023 john <jcoppens@vostro.ampr.net>
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

from pdb import set_trace as st

from math_3d import *
from another_thing import Thing

class Sphere(Thing):
    """ "Sphere" está definido por el centro y el radio.
            Sphere(['center', vec3, 'radius', float])
    """
    def __init__(self, pars = []):
        super().__init__(pars)


    def intersection(self, ray):
        center = self.params['center']
        radius = self.params['radius']
        a = 1
        b = ray.dir*(ray.loc - center)*2
        c = abs(ray.loc - center)**2 - radius**2

        D = b**2 - 4*a*c
        if D > 0:
            t1 = (-b - sqrt(D))/(2*a)
            t2 = (-b + sqrt(D))/(2*a)
            h1 = Hit(t1, (ray.at(t1) - center).normalized(), self)
            h2 = Hit(t2, (ray.at(t2) - center).normalized(), self)
            return [h1, h2]
        else:
            return []


def test_sphere():
    sph = Sphere(['center', Vec3(8, 0, 0), 'radius', 2.2])
    print(sph)

    ray = Ray(Vec3(0, 0, 0), Vec3(1, 0, 0))
    hits = sph.intersection(ray)
    for hit in hits:
        print(hit)


def main(args):
    test_sphere()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
