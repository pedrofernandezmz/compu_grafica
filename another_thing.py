#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  thing.py
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
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

from math_3d import RGB

from pdb import set_trace as st

"""
 _____ _     _
|_   _| |__ (_)_ __   __ _
  | | | '_ \| | '_ \ / _` |
  | | | | | | | | | | (_| |
  |_| |_| |_|_|_| |_|\__, |
                     |___/
"""

class Thing:
    """ Esta es la clase 'padre' de todos los elementos gráficos que siguen,
        y se encarga de tareas en común.
    """
    def __init__(self, pars = []):
        """ Convertir una lista de forma ['key1', 'val1', 'key2', 'val2'...]
            a un diccionario de tipo {'key1': 'val1', 'key2': 'key2'...}
            Notar: No hay valores por defecto posible - hay que agregarlos
            'a mano'
        """
        self.id = None
        self.params = {pars[x]: pars[x+1] for x in range(0, len(pars), 2)}

        self.reinit()


    def reinit(self):
        self.markers = []
        self.state = 0


    def to_pov_string(self):
        pass


    def __str__(self):
        return f'{self.params}'



class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(400, 300)

        self.show_all()

    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
