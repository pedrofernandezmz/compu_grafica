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
from gi.repository import Gtk

"""
 __  __            _
|  \/  | __ _ _ __| | _____ _ __
| |\/| |/ _` | '__| |/ / _ \ '__|
| |  | | (_| | |  |   <  __/ |
|_|  |_|\__,_|_|  |_|\_\___|_|

"""

class Marker:
    def __init__(self, layer, x, y, z, callback = None):
        self.mark = GooCanvas.CanvasRect(
                    parent = layer,
                    x = x - MARKER_WIDTH/2,
                    y = y - MARKER_HEIGHT/2,
                    width = MARKER_WIDTH,
                    height = MARKER_HEIGHT,
                    line_width = 2,
                    stroke_color_rgba = MARKER_BORDER_RGBA,
                    fill_color_rgba = MARKER_FILL_RGBA)

        self.lastpos = None
        self.callback = callback
        self.mark.connect('button-press-event', self.on_button_press)
        self.mark.connect('button-release-event', self.on_button_release)
        self.mark.connect('motion-notify-event', self.on_mouse_move)


    def get_pos(self):
        return (self.mark.get_property('x') + MARKER_WIDTH/2,
                self.mark.get_property('y') + MARKER_WIDTH/2)


    def on_button_press(self, src, tgt, event):
        self.lastpos = (event.x, event.y)
        return True


    def on_button_release(self, src, tgt, event):
        self.lastpos = None


    def on_mouse_move(self, src, tgt, event):
        if self.lastpos:
            dx = event.x - self.lastpos[0]
            dy = event.y - self.lastpos[1]

            xn = self.mark.get_property('x') + dx
            yn = self.mark.get_property('y') + dy
            self.mark.set_property('x', xn)
            self.mark.set_property('y', yn)
            self.lastpos = (event.x, event.y)

            if self.callback:
                self.callback(event.x, event.y)

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

        ATENCION: En este momento está deshabilitado  el parametro 'layer',
        por lo que no se puede utilizar Thing para el modelador!!!
    """
    def __init__(self, pars = {}):
        """ El único parámetro de entrada: La capa para dibujar.
        """
        # ~ self.layer = layer
        self.id = None
        self.params = pars

        self.reinit()


    def __repr__(self):
        s = ''
        for key, val in self.params.items():
            s += f'{key}: {val}, '
        return s


    def reinit(self):
        self.markers = []
        self.state = 0


    def in_use(self):
        return len(self.markers) > 0


    def to_pov_string(self):
        pass


    def __str__(self):
        return self.__str__()


    def next_state(self, x, y, z, cb):
        print(f'Adding marker {len(self.markers)}, {x:.8g}, {y:.8g} {cb}')
        marker = Marker(self.layer, x, y, z, cb)
        self.markers.append(marker)


    def params_from_token(self, tkn):
        """ Convertir una lista de forma ['key1', 'val1', 'key2', 'val2'...]
            a un diccionario de tipo {'key1': 'val1', 'key2': 'key2'...}
            Notar: No hay valores por defecto posible - hay que agregarlos
            'a mano'
        """
        self.params = {tkn[idx]: tkn[idx+1] for idx in range(0, len(tkn), 2)}



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
