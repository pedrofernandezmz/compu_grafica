#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  intersect.py
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

#   escena.py: Mostrar la escena que implementaremos para el mini-renderizador


from math_3d import *
from math import tan, radians

import pylab as plt

from pdb import set_trace as st

from thing import Thing
from sphere import Sphere
from box import Box
from light import Light
from camera import Camera
from tracer import ray_generator, tracer

from PIL import Image


# ~ def ray_generator(w, h, loc, angle, x0 = 0, y0 = 0, x1 = 100, y1 = 100):
    # ~ """ Generador de rayos. Cada iteración devuelve un rayo, que contiene
        # ~ la ubicación (ray.loc) y dirección (ray.dir).
    # ~ """
    # ~ phys_width = tan(radians(angle)/2) * 2 # * abs(loc.x)
    # ~ pixelsize = phys_width/w

    # ~ for l in range(int(h*y0/100), int(h*y1/100)):
        # ~ for c in range(int(w*x0/100), int(w*x1/100)):
            # ~ z = c - (w//2) + 0.5
            # ~ y = l - (h//2) + 0.5
            # ~ z *= pixelsize
            # ~ y *= pixelsize
            # ~ direction = Vec3(1 - loc.x,
                             # ~ y - loc.y,
                             # ~ z - loc.z)

            # ~ yield c, h-l, Ray(loc, direction.normalized())


def test_ray_generator():
    raygen = ray_generator(80, 60, Vec3(0, 0, 0), 50)
    ys = []; zs = []
    for y, z, ray in raygen:
        ys.append(ray.dir.y)
        zs.append(ray.dir.z)

    print(ys, zs)
    plt.scatter(ys, zs)
    plt.show()


def test_sphere_intersection_text():
    loc = Vec3(0, 0, 0)
    sph = Sphere(Vec3(8, 0, 0), 3)

    raygen = ray_generator(8, 6, loc, 50)
    for x, y, ray in raygen:
        if x == 0: print()
        print('\u2588'*2 if sph.intersection(ray) else '\u2591'*2, end = '')


def test_sphere_intersection_image():
    things  = [Sphere(['center', Vec3(12, 2, 0), 'radius', 3]),
               Sphere(['center', Vec3(14, 3, -3), 'radius', 2])]
    lights  = [Light(['loc', Vec3(0, 33, 44), 'rgb', RGB('White')])]
    cameras = [Camera(['location', Vec3(0, 0, 0), 'look_at', Vec3(10, 0, 0),
                      'up', Vec3(0, 1, 0)])]

    tracer(200, 150, things, lights, cameras)



def test_box_intersection_text():
    boxsize = Vec3(4)
    loc = Vec3(8, 0, 0)
    box = Box(loc - boxsize/2, loc + boxsize/2)
    print(box)

    raygen = ray_generator(8, 6, loc, 50)
    for x, y, ray in raygen:
        if x == 0: print()
        print('\u2588'*2 if box.intersection(ray) else '\u2591'*2, end = '')


def main(args):
    # ~ test_ray_generator()
    # ~ test_sphere_intersection_text()
    test_sphere_intersection_image()
    # ~ test_box_intersection_text()



if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
