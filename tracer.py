#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  tracer.py
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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


from thing import Thing
from sphere import Sphere
from box import Box
from cylinder import Cylinder
from light import Light
from camera import Camera
from math_3d import Vec3, RGB, Ray, Hits, EPSILON

from math import tan, radians
from pdb import set_trace as st
import pylab as plt

from PIL import Image

AMBIENT = 0.25

def ray_generator(w, h, loc, angle,
                  x0 = None, x1 = None, y0 = None, y1 = None):
    """ Generador de rayos. Cada iteración devuelve un rayo, que contiene
        la ubicación (ray.loc) y dirección (ray.dir).
    """
    if x0 is None: x0 = 0
    if y0 is None: y0 = 0
    if x1 is None: x1 = w
    if y1 is None: y1 = h

    phys_width = tan(radians(angle)/2) * 2
    pixelsize = phys_width/w

    for l in range(y0, y1):
        for c in range(x0, x1):
            z = c - (w//2) + 0.5
            y = l - (h//2) + 0.5
            z *= pixelsize
            y *= pixelsize
            direction = Vec3(1 - loc.x,
                             y - loc.y,
                             z - loc.z)

            yield w-1-c, h-1-l, Ray(loc, direction.normalized())


def tracer(w, h, catalog, **kwargs):
    cameras = catalog['cameras']
    things = catalog['things']
    lights = catalog['lights']

    assert len(cameras) == 1

    camera = cameras[0]
    img = Image.new('RGB', (w, h), color="#000")
    raygen = ray_generator(w, h, camera.params['location'],
                                 camera.params['angle'], **kwargs)

    hitlist = Hits()
    for x, y, ray in raygen:
        hitlist.clear()
        # Podemos ver al objeto?
        for thingie in things:
            hits = thingie.intersection(ray)
            for hit in hits:
                hitlist.add_hit(hit)

        t, normal, thing = hitlist.nearest().as_tuple()

        if t != float('inf'):
            # Parece que lo vemos. Ahora, llega la luz al objeto?
            hit_color = RGB(0, 0, 0)
            hit_loc = ray.at(t)
            thing_rgb = thing.params['rgb']

            # hit_color accumulates all light source effects
            for light in lights:
                light_loc = light.params['loc']
                light_rgb = light.params['rgb']
                # lanzamos un rayo desde la luz hasta el punto de impacto
                # para determinar si algún objeto obstruye la luz
                light_ray = Ray(hit_loc, (light_loc - hit_loc).normalized())

                fact = (1 - AMBIENT)
                for thingie in things:
                    hits = thingie.intersection(light_ray)
                    for hit in hits:
                        if hit.t > EPSILON:
                            fact = 0        # (1 - AMBIENT)
                            break

                    if fact == 0:
                        break

                cos1 = (AMBIENT +
                        normal * (light_loc - ray.at(t)).normalized() * fact)
                hit_color = hit_color + thing_rgb.reflect(light_rgb) * cos1

            # Combinarlo con la luz ambiente
            img.putpixel((x, y), hit_color.as_pil())
    img.show()


def test_ray_generator():
    raygen = ray_generator(60, 45, Vec3(0, 0, 0), 60)
    ys = []; xs = []
    for x, y, ray in raygen:
        print(f'{x:3}, {y:3}, {ray.dir.x:.4f}, {ray.dir.y:.4f}, {ray.dir.z:.4f}')
        xs.append(ray.dir.y)
        ys.append(ray.dir.z)

    plt.scatter(xs, ys, marker='.')
    plt.grid(True)
    plt.show()


def test_sphere_intersection_text():
    loc = Vec3(0, 0, 0)
    sph = Sphere(['center', Vec3(8, 0, 0), 'radius', 3, rgb, RGB(1, 1, 0)])

    raygen = ray_generator(8, 6, loc, 50)
    for x, y, ray in raygen:
        if x == 0: print()
        print('\u2588'*2 if sph.intersection(ray) else '\u2591'*2, end = '')


def test_sphere_intersection_image():
    things = [
        Sphere(['center', Vec3(12, 0, 0),  'radius', 3, 'rgb', RGB('Yellow')]),
        Sphere(['center', Vec3(14, 0, -5), 'radius', 2, 'rgb', RGB('Green')]),
        Sphere(['center', Vec3(10, 0, 4),  'radius', 2, 'rgb', RGB('Orange')]),
        Sphere(['center', Vec3( 9, 4, 3),  'radius', 2, 'rgb', RGB('Blue')])
    ]
    lights = [
        Light(['loc', Vec3(0, 33, 44), 'rgb', RGB('White')])
    ]
    cameras = [
        Camera(['location', Vec3(0, 0, 0),
                'look_at',  Vec3(10, 0, 0),
                'up',       Vec3(0, 1, 0)])
    ]

    tracer(200, 150, things, lights, cameras)


def test_multi_lights():
    catalog = {
    'things': [
        Sphere(['center', Vec3(12, 0, 0), 'radius', 3, 'rgb', RGB('White')])
    ],
    'lights': [
        Light(['loc', Vec3(10, 0, 18), 'rgb', RGB('Red')]),
        Light(['loc', Vec3(10, 10, 0), 'rgb', RGB('Green')]),
        Light(['loc', Vec3(10, -10, 0), 'rgb', RGB('Blue')]),
        Light(['loc', Vec3(12, 0, -18), 'rgb', RGB('Yellow')])
    ],
    'cameras': [
        Camera(['location', Vec3(0, 0, 0),
                'look_at',  Vec3(10, 0, 0),
                'up',       Vec3(0, 1, 0)])
    ]}

    tracer(400, 300, catalog)
                     # ~ x0 = 0, x1 = 100, y0 = 50, y1 = 51)


def test_shadows():
    catalog = {
    'things': [
        Sphere(['center', Vec3(12, 0, 5), 'radius', 3, 'rgb', RGB('Yellow')]),
        Sphere(['center', Vec3(12, 0, -3), 'radius', 1, 'rgb', RGB('Orange')])
    ],
    'lights': [
        Light(['loc', Vec3(12, 0, -20), 'rgb', RGB('White')])
    ],
    'cameras': [
        Camera(['location', Vec3(0, 0, 0),
                'look_at',  Vec3(10, 0, 0),
                'up',       Vec3(0, 1, 0)])
    ]}

    tracer(400, 300, catalog) #, x0 = 250, x1 = 251, y0 = 150, y1 = 151)


def test_box_intersection_text():
    boxsize = Vec3(4)
    loc = Vec3(8, 0, 0)
    box = Box(loc - boxsize/2, loc + boxsize/2)

    raygen = ray_generator(8, 6, loc, 50)
    for x, y, ray in raygen:
        if x == 0: print()
        print('\u2588'*2 if box.intersection(ray) else '\u2591'*2, end = '')



class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(400, 300)

        self.show_all()

    def run(self):
        Gtk.main()


def main(args):
    # ~ test_ray_generator()
    # ~ test_sphere_intersection_text()
    # ~ test_sphere_intersection_image()
    # ~ test_multi_lights()
    # ~ test_misc()
    test_shadows()
    # ~ test_box_intersection_text()
    return 0                        # No permitimos la ventana para hacer pruebas

    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
