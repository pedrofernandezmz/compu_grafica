#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  math_3d.py
#
#  Copyright 2021 John Coppens <john@jcoppens.com>
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

#   math_3d: Librería con clases/funciones necesarios para el raytracer


from math import sqrt
from pdb import set_trace as st
from numbers import Number


EPSILON = 1e-6      # Constante de 'umbral' de errores permitidos

Colors = {
    'Black':    [0, 0, 0],
    'White':    [1, 1, 1],

    'Red':      [1, 0, 0],
    'DarkRed':  [0.5, 0, 0],
    'Green':    [0, 1, 0],
    'DarkGreen':[0, 0.5, 0],
    'Blue':     [0, 0, 1],
    'DarkBlue': [0, 0, 0.5],

    'Yellow':   [1, 1, 0],
    'Purple':   [1, 0, 1],
    'Cyan':     [0, 1, 1],
    'Orange':   [1, 0.5, 0],

    'Salmon':   [0.98, 0.5, 0.447],
    'Rosa':     [1, 0.75, 0.8],
    'Coral':    [1, 0.5, 0.313],
    'Gold':     [1, 215, 0.81],
    'Violet':   [0.93, 0.51, 0.93],
    'Olive':    [0.5, 0.5, 0],
    'Chocolate':[0.82, 0.41, 0.12],

    'Gray25':   [0.25, 0.25, 0.25],
    'Gray':     [0.5, 0.5, 0.5],
    'Gray75':   [0.75, 0.75, 0.75]
}

class RGB:
    """ Representación de un color, mediante los componentes R, G, B
        Los valores de los componentes están entre 0 y 1 (incluidos)
        Datos pueden ingresar como:
            3 parametros,
                r, g, b son floats
            1 parametro,
                si es entero, debe ser un valor entre 0x0 y 0xffffff+1,
                    representando 3 bytes R, G, B
                si es string, los formatos permitidos son:
                    #rgb  (3 nibbles)
                    #rrggbb  (3 bytes)
                    #rrrrggggbbbb   (3 words)
    """
    def __init__(self, r, g = None, b = None):
        if isinstance(r, str):
            if r in Colors:
                self._r, self._g, self._b = Colors[r]

            elif r[0] == '#':
                if len(r) == 4:                 # #rgb   #7AF
                    self._r = int(r[1], 16) / 15
                    self._g = int(r[2], 16) / 15
                    self._b = int(r[3], 16) / 15

                elif len(r) == 7:               # #rrggbb    #1122EE
                    self._r = int(r[1:3], 16) / 255
                    self._g = int(r[3:5], 16) / 255
                    self._b = int(r[5:], 16)  / 255

                elif len(r) == 13:              # #1111cccc5555    #12AF33EEAF76
                    self._r = int(r[1:5], 16) / 65535
                    self._g = int(r[5:9], 16) / 65535
                    self._b = int(r[9:], 16)  / 65535

                else:
                    print('Formato de la cadena debe ser el nombre de un color,'
                          '#rgb, #rrggbb, ó #rrrrggggbbbb')
                    exit(1)

        elif isinstance(r, int) and (g is None) and (b is None):
            self._r = (r // 65536) / 255
            self._g = ((r // 256) % 256) / 255
            self._b = (r % 256) / 255

        else:
            self._r, self._g, self._b = r, g, b


    def get_r(self):
        return self._r

    def get_g(self):
        return self._g

    def get_b(self):
        return self._b

    def set_r(self, rr):
        self._r = rr

    def set_g(self, gg):
        self._g = gg

    def set_b(self, b):
        self._b = bb

    r = property(get_r, set_r)
    g = property(get_g, set_g)
    b = property(get_b, set_b)


    def __str__(self):
        return f"RGB({self._r:.6g}, {self._g:.6g}, {self._b:.6g})"


    def limit(self):
        """ Limita los componentes al rango de 0.0 .. 1.0
        """
        self._r = max(0, min(1, self._r))
        self._g = max(0, min(1, self._g))
        self._b = max(0, min(1, self._b))
        return self


    def __add__(a, b):
        return RGB(a._r + b._r, a._g + b._g, a._b + b._b).limit()


    def __mul__(a, b):
        return RGB(a._r*b, a._g*b, a._b*b).limit()


    def __neg__(a):
        return RGB(-a._r, -a._g, -a._b)


    def __truediv__(a, b):
        return RGB(a._r/b, a._g/b, a._b/b).limit()


    def reflect(self, light_rgb):
        return RGB(light_rgb.r * self._r,
                   light_rgb.g * self._g,
                   light_rgb.b * self._b)


    def add(self, rgb):
        self._r += rgb._r
        self._g += rgb._g
        self._b += rgb._b
        self.limit()
        return self


    def subtract(self, rgb):
        self._r -= rgb.r
        self._g -= rgb.g
        self._b -= rgb.b
        self.limit()
        return self


    def multiply(self, factor):
        self._r *= factor
        self._g *= factor
        self._b *= factor
        self.limit()
        return self


    def divide(self, factor):
        self._r /= factor
        self._g /= factor
        self._b /= factor
        self.limit()
        return self


    def as_list(self):
        return [self._r, self._g, self._b]


    def as_pil(self):
        return (round(self._r * 255),
                round(self._g * 255),
                round(self._b * 255))



class Vec2:
    """ Representación de una ubicación en un plano, ó una dirección de
        un vector (también en 2D).
            Parameters del constructor:
                (float1, float2)
                ([float1, float2])
                (Vec2)
    """
    def __init__(self, x, y = None):
        if isinstance(x, Vec2):
            self._x, self._y = x.x, x.y

        elif isinstance(x, list) or isinstance(x, tuple):
            if len(x) == 2:
                self._x, self._y = x
            else:
                print('Vec2 parameter list or tuple is not of length 2')

        elif (y == None) and isinstance(x, Number):
            self._x = x; self._y = x

        elif (isinstance(x, Number) and
              isinstance(y, Number)):
            self._x, self._y = x, y

        else:
            print('x or y is not a number:')
            print(type(_x), type(_y))


    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, xx):
        self._x = xx

    def set_y(self, yy):
        self._y = yy

    x = property(get_x, set_x)
    y = property(get_y, set_y)

    def __str__(self):
        return f"Vec2(X: {self._x:g}, Y: {self._y:_g})"


    def as_tuple(self):
        return (self._x, self._y)


    def as_list(self):
        return [self._x, self._y]


class Vec3:
    """ Representación de una ubicación en el espacio, ó una dirección de
        un vector.
            Parameters del constructor:
                (float1, float2, float3)
                ([float1, float2, float3])
                (Vec3)
    """
    def __init__(self, x, y = None, z = None):
        if isinstance(x, Vec3):
            self._x, self._y, self._z = x.x, x.y, x.z

        elif isinstance(x, list) or isinstance(x, tuple):
            if len(x) == 3:
                self._x, self._y, self._z = x
            else:
                print('Vec3 parameter list or tuple is not of length 3')

        elif (y == None) and (z == None) and isinstance(x, Number):
            self._x = x; self._y = x; self._z = x

        elif (isinstance(x, Number) and
              isinstance(y, Number) and
              isinstance(z, Number)):
            self._x, self._y, self._z = x, y, z

        else:
            print('x, y, or z is not a number:')
            print(type(x), type(y), type(z))
            exit(1)


    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_z(self):
        return self._z

    def set_x(self, xx):
        self._x = xx

    def set_y(self, yy):
        self._y = yy

    def set_z(self, zz):
        self._z = zz

    x = property(get_x, set_x)
    y = property(get_y, set_y)
    z = property(get_z, set_z)


    def __str__(self):
        return f"Vec3(X: {self.x:g}, Y: {self._y:g}, Z: {self._z:g})"


    def __add__(self, v3):
        return Vec3(self._x + v3.x, self._y + v3.y, self._z + v3.z)


    def __sub__(self, v3):
        return Vec3(self._x - v3.x, self._y - v3.y, self._z - v3.z)


    def __mul__(self, v3):
        if isinstance(v3, Vec3):
            return self._x*v3.x + self._y*v3.y + self._z*v3.z
        else:
            return Vec3(self._x*v3, self._y*v3, self._z*v3)


    def __div__(self, v3):
        assert isinstance(v3, Number)
        return Vec3(self._x*v3, self._y*v3, self._z*v3)


    def __matmul__(self, v3):
        return Vec3(self._y * v3.z - self._z * v3.y,
                    self._z * v3.x - self._x * v3.z,
                    self._x * v3.y - self._y * v3.x)


    def __neg__(v3):
        return Vec3(-v3.x, -v3.y, -v3.z)


    def __truediv__(self, f):
        return Vec3(self._x/f, self._y/f, self._z/f)


    def __abs__(self):
        return sqrt(self._x * self._x + self._y * self._y + self._z * self._z)


    def add(self, vec3):
        self._x += vec3.x
        self._y += vec3.y
        self._z += vec3.z
        return self


    def subtract(self, vec3):
        self._x -= vec3.x
        self._y -= vec3.y
        self._z -= vec3.z
        return self


    def cross(self, v3):
        x = self._y * v3.z - self._z * v3.y
        y = self._z * v3.x - self._x * v3.z
        z = self._x * v3.y - self._y * v3.x
        self._x = x; self._y = y; self._z = z
        return self


    def normalized(self):
        d = abs(self)
        self._x /= d
        self._y /= d
        self._z /= d
        return self
    
    def length_squared(self):
        return self._x**2 + self._y**2 + self._z**2
        
    def length(self):
    	return sqrt(self._x**2 + self._y**2 + self._z**2)
    
    def dot(self, v3):
        return self._x * v3.x + self._y * v3.y + self._z * v3.z

    def as_tuple(self):
        return (self._x, self._y, self._z)


    def as_list(self):
        return [self._x, self._y, self._z]


    def as_csv(self):
        return f'{self._x},{self._y},{self._z}'


X = Vec3(1, 0, 0)
Y = Vec3(0, 1, 0)
Z = Vec3(0, 0, 1)


class Ray:
    """ Caracteristicas del rayo:
            - Origen
            - Dirección
    """
    def __init__(self, loc, dir):
        self.loc, self.dir = Vec3(loc), Vec3(dir)


    def __str__(self):
        return "Ray: loc: {}, dir: {}".format(self.loc, self.dir)


    def at(self, t):
        return self.loc + self.dir * t



class Hit:
    """ Clase que agrupa los datos de un punto de impact en un objeto
    """
    def __init__(self, t, normal, thing):
        self.t, self.normal, self.thing = t, normal, thing


    def __str__(self):
        return f'Hit: t = {self.t}'


    def as_tuple(self):
        return self.t, self.normal, self.thing



class Hits:
    """ Tabla de los impactos del rayo en el objeto
        <hits> es la lista de los impactos (instancias de Hit). Cada impacto
            consta del punto de impacto, la normal en el este mismo punto,
            y <ref> es una referencia a la instancia del objeto (ej. la esfera)
    """
    def __init__(self):
        self.hits = []


    def __str__(self):
        s = '\nHit(s):\n'
        for hit in self.hits:
            s += f'  {str(hit.thing)} @ {hit.t} (normal: {hit.normal}\n'
        return s


    def add_hit(self, hit):
        self.hits.append(hit)


    def nr_hits(self):
        return len(self.hits)


    def empty(self):
        return len(self.hits) == 0


    def clear(self):
        self.hits = []


    def nearest(self):
        nearest = Hit(float('inf'), None, None)
        for hit in self.hits:
            if (hit.t >= 0) and (hit.t < nearest.t):
                nearest = hit
        return nearest


def test_rgb():
    for test in ['RGB(0.1, 0.2, 0.3)',
                 'RGB("#123")',
                 'RGB("DarkGreen")',
                 'RGB("#445566")',
                 'RGB("#aaaabbbbffff")',
                 'RGB(0x123456)',
                 'RGB(0.1, 0.2, 0.3).add(RGB(0.5, 0.5, 0.5))',
                 'RGB(0.1, 0.2, 0.3) + (RGB(0.5, 0.5, 0.5))',
                 'RGB(0.5, 0.6, 0.7) * 0.5',
                 'RGB(0.4, 0.6, 0.7) * 2',
                 'RGB(0.1, 0.2, 0.3) / 2',
                 '-RGB(0.1, 0.2, 0.3)']:
        print(f'{test} => ', end = '')
        print(f'{eval(test)}')
    return


def test_vec3():
    for test in ['Vec3(1, 2, 3)',
                 'Vec3(4)',
                 'Vec3(1, 2, 3).normalized()',
                 'abs(Vec3(1, 2, 3).normalized())',
                 'Vec3([0.11, 0.22, 0.33])',
                 'Vec3(1, 2, 3) * Vec3(1, 2, 3)',
                 'Vec3(9, 2, 7) * Vec3(4, 8, 10)',
                 'Vec3(9, 2, 7) * (Vec3(6, 10, 12) - Vec3(2, 2, 2))',
                 'Vec3(2.185817147601556, 1.3114902885609336, -5.0) * (Vec3(0, 0, -5) - Vec3(0, 0, 4)) * 2',
                 'Vec3(1, 2, 3) * 2',
                 'Vec3(1, 2, 3) / 2',
                 'Vec3(1, 2, 3).add(Vec3(0.1, 0.2, 0.3))',
                 'Vec3(1, 2, 3) + (Vec3(0.1, 0.2, 0.3))',
                 'Vec3(1, 2, 3).subtract(Vec3(0.1, 0.2, 0.3))',
                 'Vec3(1, 2, 3) - (Vec3(0.1, 0.2, 0.3))',
                 'Vec3(1, 2, 3) @ (Vec3(0.1, 0.2, 0.3))',
                 'Vec3(1, 2, 3).as_tuple()']:
        print(f'{test} => ', end = '')
        print(f'{eval(test)}')


def test_vec2():
    for test in ['Vec2(1, 2)',
                 'Vec2(4)',
                 'Vec2([0.11, 0.22])',
                 'Vec2(1, 2).as_tuple()']:
        print(f'{test} => ', end = '')
        print(f'{eval(test)}')


def test_hits():
    """ Comprobar si funciona lista de impactos. Como tipo de objeto usaremos
        'int' (en lugar de Sphere u otro)
    """
    hits = Hits()
    hits.add_hit(Hit(3, Vec3(1, 2, 3), int))
    hits.add_hit(Hit(2, Vec3(1.1, 2.2, 3.3), int))
    hits.add_hit(Hit(5, Vec3(1.11, 2.22, 3.33), int))
    hits.add_hit(Hit(-7, Vec3(9, 8, 7), int))
    print(hits)

    print('Nearest:', hits.nearest())


def test_reflect():
    for surface in [RGB(0, 0, 0), RGB(1, 1, 1),
                    RGB(1, 0, 0), RGB(0, 1, 0), RGB(0, 0, 1),
                    RGB(1, 0, 1)]:
        print(f'Superficie {surface}:')
        for light in [RGB(0, 0, 0), RGB(1, 1, 1),
                      RGB(0.5, 0.5, 0.5)]:
            print(f'     refleja {light}) como {surface.reflect(light)}')


def main(args):
    # ~ test_rgb()
    # ~ test_reflect()
    # ~ test_vec2()
    # ~ test_vec3()
    # ~ test_hits()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
