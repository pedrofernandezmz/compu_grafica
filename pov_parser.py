#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  testpp.py
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

import pyparsing as pp
from math_3d import Vec2, Vec3, RGB, Colors
from pdb import set_trace as st

"""
 ____
|  _ \ __ _ _ __ ___  ___ _ __
| |_) / _` | '__/ __|/ _ \ '__|
|  __/ (_| | |  \__ \  __/ |
|_|   \__,_|_|  |___/\___|_|

"""

def make_pov_parser(which = None):
    """ Este método convierte la salida del parser en:
            camera,
            lista de luces,
            lista de objetos
    """
    unsigned = pp.Word(pp.nums)
    signed = pp.Optional(pp.one_of("+ -")) + unsigned
    floatn = pp.Combine(signed + pp.Optional("." + unsigned))
    floatn = floatn.set_parse_action(lambda tkns: float(tkns[0]))
    block_open = pp.Suppress('{')
    block_end  = pp.Suppress('}')
    comma = pp.Suppress(',')

    vector2 = pp.Group(pp.Suppress("<") +
                            floatn + pp.Suppress(",") +
                            floatn +
                      pp.Suppress(">"))
    vector2.set_parse_action(lambda t: Vec2(*t[0]))

    vector3 = pp.Group(pp.Suppress("<") +
                            floatn + pp.Suppress(",") +
                            floatn + pp.Suppress(",") +
                            floatn +
                      pp.Suppress(">"))
    vector3.set_parse_action(lambda t: Vec3(*t[0]))

    # Color by color name   eg. color Orange
    color_name = pp.one_of(' '.join(Colors))
    color_color = pp.Suppress(pp.Keyword('color')) + color_name
    color_color.set_parse_action(lambda tkn: RGB(*Colors[tkn[0]]))

    # Color by rgb          eg. rgb <0.2, 0.4, 0.5>
    color_rgb = pp.Suppress(pp.Keyword('rgb')) + vector3
    color_rgb.set_parse_action(lambda tkn: RGB(*tkn[0].as_list()))

    color = color_rgb ^ color_color

    directive = pp.Group(
                '#include' +
                pp.QuotedString(quote_char = '"') +
                pp.Suppress(pp.LineEnd()))

    # TODO: suppress shouldn't be here
    pigment = (pp.Suppress(pp.Keyword('pigment')) +
                block_open +
                    color +
                block_end)
    pigment.set_parse_action(lambda t: ['rgb', t[0]])

    obj_modifiers = (pp.ZeroOrMore(color) ^
                     pigment)

    # TODO: Dirty trick: add 'loc' name
    light_source = pp.Group(pp.Keyword('light_source') +
                block_open +
                    vector3 + comma +
                    color +
                block_end).set_parse_action(lambda t: t[0].insert(1, 'loc'))
    light_source.add_parse_action(lambda t: t[0].insert(3, 'rgb'))

    camera_look_at  = (pp.Keyword('look_at') + vector3)
    camera_up       = (pp.Keyword('up') + vector3)
    camera_angle    = (pp.Keyword('angle') + floatn)
    camera_location = (pp.Keyword('location') + vector3)

    camera = pp.Group(
                pp.Keyword('camera') +
                block_open +
                    (camera_location & camera_look_at & camera_up & camera_angle) +
                block_end)

    box = pp.Group(
                pp.Keyword('box') +
                block_open +
                    vector3 + pp.Suppress(',') +              # Box corner 1
                    vector3 +                                 # Box corner 2
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(2, 'corner2'))
    box.add_parse_action(lambda t: t[0].insert(1, 'corner1'))

    sphere = pp.Group(
                pp.Keyword('sphere') +
                block_open +
                    vector3 + pp.Suppress(',') +            # Sphere center
                    floatn +                                # Sphere radius
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(2, 'radius'))
    sphere.add_parse_action(lambda t: t[0].insert(1, 'center'))

    torus = pp.Group(
                pp.Keyword('torus') +
                block_open +
                    floatn + pp.Suppress(',') +         # Major axis
                    floatn +                            # Minor axis
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(2, 'minor'))
    torus.add_parse_action(lambda t: t[0].insert(1, 'major'))

    plane = pp.Group(
                pp.Keyword('plane') +
                block_open +
                    vector3 + pp.Suppress(',') +            # Plane normal
                    floatn +                                # Distance from origin
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(2, 'normal'))
    plane.add_parse_action(lambda t: t[0].insert(1, 'distance'))

    cylinder = pp.Group(
                pp.Keyword('cylinder') +
                block_open +
                    vector3 + pp.Suppress(',') +            # Cylinder radius
                    vector3 + pp.Suppress(',') +            # Base center point
                    floatn +                                # Cap center point
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(3, 'radius'))
    cylinder.add_parse_action(lambda t: t[0].insert(2, 'cap_point'))
    cylinder.add_parse_action(lambda t: t[0].insert(1, 'base_point'))

    disc = pp.Group(
                pp.Keyword('disc') +
                block_open +
                    vector3 + pp.Suppress(',') +            # Disc center
                    vector3 + pp.Suppress(',') +            # Disc normal
                    floatn +                                # Radius
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(3, 'radius'))
    disc.add_parse_action(lambda t: t[0].insert(2, 'normal'))
    disc.add_parse_action(lambda t: t[0].insert(1, 'center'))

    cone = pp.Group(
                pp.Keyword('cone') +
                block_open +
                    vector3 + pp.Suppress(',') +            # Base center
                    floatn + pp.Suppress(',') +             # Base radius
                    vector3 + pp.Suppress(',') +            # Cap center
                    floatn +                                # Cap radius
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(4, 'base_radius'))
    cone.add_parse_action(lambda t: t[0].insert(3, 'base_point'))
    cone.add_parse_action(lambda t: t[0].insert(2, 'cap_radius'))
    cone.add_parse_action(lambda t: t[0].insert(1, 'cap_point'))

    triangle = pp.Group(
                pp.Keyword('triangle') +
                block_open +
                    vector3 + pp.Suppress(',') +            # Triangle corner 1
                    vector3 + pp.Suppress(',') +            # Corner 2
                    vector3 +                               # Corner 3
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(3, 'corner3'))
    triangle.add_parse_action(lambda t: t[0].insert(2, 'corner2'))
    triangle.add_parse_action(lambda t: t[0].insert(1, 'corner1'))

    prism = pp.Group(
                pp.Keyword('prism') +
                block_open +
                    floatn + pp.Suppress(',') +         # Height 1
                    floatn + pp.Suppress(',') +         # Height 2
                    pp.Group(pp.counted_array(pp.Suppress(',') + vector2)) +
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(3, 'corners'))
    prism.add_parse_action(lambda t: t[0].insert(2, 'height2'))
    prism.add_parse_action(lambda t: t[0].insert(1, 'height1'))

    things = (box ^ sphere ^ plane ^ triangle ^ cylinder ^ cone ^ disc ^
              torus ^ prism)

    polygon = pp.Group(
                pp.Keyword('polygon') +
                block_open +
                    pp.Group(pp.counted_array(pp.Suppress(',') + vector2)) +
                    obj_modifiers +
                block_end).set_parse_action(lambda t: t[0].insert(1, 'corners'))

    things = (box ^ sphere ^ plane ^ triangle ^ cylinder ^ cone ^ disc ^
              torus ^ prism ^ polygon)

    if which:
        parser = eval(which)
    else:
        parser = pp.OneOrMore(directive ^ light_source ^ things ^ camera)

    return parser


def parser(src):
    psr =  make_pov_parser()
    return psr.parse_string(src)
"""
 _____         _                     _   _
|_   _|__  ___| |_   _ __ ___  _   _| |_(_)_ __   ___  ___
  | |/ _ \/ __| __| | '__/ _ \| | | | __| | '_ \ / _ \/ __|
  | |  __/\__ \ |_  | | | (_) | |_| | |_| | | | |  __/\__ \
  |_|\___||___/\__| |_|  \___/ \__,_|\__|_|_| |_|\___||___/

"""

def test_light_source():
    parser = make_pov_parser('light_source')
    r = parser.parse_string('light_source { <1, 2, 3>, rgb <0.1, 0.2, 0.3>}')


def test_thing(thing, pars):
    """ Comprobar el funcionamiento de 'thing' (a reemplazar por una de las
        primitivas (sphere, box, etc)
    """
    parser = make_pov_parser(thing)
    try:
        parsed = parser.parse_string(
                thing + '{' + pars + '\n'
                        '      pigment {\n'
                        '          rgb <0.11, 0.22, 0.33>\n'
                        '      }\n'
                        '}\n')

    except pp.ParseException as err:
        print(err.line)
        print(" "*(err.column-1) + "^")
        print(err)

    return parsed


def test_camera():
    from random import shuffle
    parser = make_pov_parser('camera')
    cam_params = ['location <1, 2, 3>',
                  'look_at <4, 5, 6>',
                  'up <7, 8, 9>',
                  'angle 66']

    print('\nRandom order of parameters:')
    for n in range(4):
        shuffle(cam_params)
        cam_s = (f'camera {{{cam_params[0]} {cam_params[1]} {cam_params[2]} '
                 f'{cam_params[3]}}}')
        print(cam_s)
        print(parser.parse_string(cam_s))

    print('\nTest if missing parameters are detected:'
          '\n' + '-'*70 +
          '\nLa excepción que sigue es normal!'
          '\n' + '-'*70)
    try:
        cam_s = 'camera {location <1, 2, 3> up <7, 8, 9> angle 66}'
        print(parser.parse_string(cam_s))

    except pp.ParseException as err:
        print(err.explain())


def test_basics(rule, cases):
    """ Este utilitario es común a los tests de colores y vectores que siguen.
    """
    print('Testing', rule)
    parser = make_pov_parser(rule)
    for case in cases:
        print(f'    {case} => ', end = '')
        parsed = parser.parse_string(case)
        print(f'{parsed}')
        if rule.startswith('vector'):
            print(f'{parsed[0].x}')
            print(f'{parsed[0].y}')
            print(f'{parsed[0].z}')
        else:
            print(f'{parsed[0].r}')
            print(f'{parsed[0].g}')
            print(f'{parsed[0].b}')


def test_colors():
    test_basics('color', ['color Orange',
                          'rgb <0.2, 0.3, 0.4>'])


def test_vectors():
    test_basics('vector2', ['<0.22, 0.33>',
                            '<0.111, 0.222>'])
    test_basics('vector3', ['<0.22, 0.33, 0.44>'])


def main(args):
    # ~ test_vectors()
    # ~ test_colors()

    # ~ test_light_source()
    # ~ print(test_thing('box',      '<1, 2, 3>, <2, 3, 4>'))
    # ~ print(test_thing('sphere',   '<1, 2, 3>, 3.5'))
    # ~ print(test_thing('triangle', '<1, 2, 3>, <1.5, 2.6, 3.7>, <2, 3.5, 6>'))
    # ~ print(test_thing('cylinder', '<1, 2, 3>, <1.5, 2.6, 3.7>, 3.5'))
    # ~ print(test_thing('disc',     '<1, 2, 3>, <1.5, 2.6, 3.7>, 3.5'))
    # ~ print(test_thing('cone',     '<1, 2, 3>, 0.5, <1.5, 2.6, 3.7>, 3.5'))
    # ~ print(test_thing('plane',    '<1, 2, 3>, 3.5'))
    # ~ print(test_thing('torus',    '3.5, 0.5'))
    # ~ print(test_thing('prism',    '0.5, 3.5, 3, <1, 2>, <2, 3>, <3, 4>'))
    # ~ print(test_thing('polygon',  '4, <1, 2>, <2, 3>, <3, 4>, <4, 5>'))
    test_camera()
    return 0

    with open('scenes/test_scene2.pov', 'r') as povf:
        source = povf.read()

        povparser = make_pov_parser()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
