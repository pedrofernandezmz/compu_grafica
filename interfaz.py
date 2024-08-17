#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  interfaz.py
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


import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from main_menu import Main_menu
from aux import confirmed, warning, open_file
from pov_parser import parser
from camera import Camera
from light import Light
from box import Box
from sphere import Sphere
from cylinder import Cylinder
from tracer import tracer

import subprocess as sp

from pdb import set_trace as st

WIDTH  = 400
HEIGHT = 300
#WIDTH  = 1920
#HEIGHT = 1080


"""
 __  __       _
|  \/  | __ _(_)_ __      _ __ ___   ___ _ __  _   _
| |\/| |/ _` | | '_ \    | '_ ` _ \ / _ \ '_ \| | | |
| |  | | (_| | | | | |   | | | | | |  __/ | | | |_| |
|_|  |_|\__,_|_|_| |_|___|_| |_| |_|\___|_| |_|\__,_|
                    |_____|
"""



class Pov_editor(Gtk.Frame):
    def __init__(self):
        super().__init__(
                    label = '',
                    label_xalign = 0.5,
                    margin = 5)

        self.active_file = None

        self.buffer = Gtk.TextBuffer()
        self.viewer = Gtk.TextView(
                    margin = 6,
                    buffer = self.buffer,
                    monospace = True)

        scroller = Gtk.ScrolledWindow()
        scroller.add(self.viewer)

        vbox = Gtk.VBox()
        vbox.pack_start(scroller, True, True, 0)

        self.add(vbox)


    def get_text(self):
        return self.buffer.get_text(
                    self.buffer.get_start_iter(),
                    self.buffer.get_end_iter(),
                    False)


    def load_file(self, fname):
        with open(fname, 'r') as srcf:
            self.buffer.set_text(srcf.read())
            self.set_label(fname)
            self.active_file = fname


    def save_file_as(self, fname):
        with open(fname, 'w') as dstf:
            dstf.write(self.get_text())
            self.set_label(fname)
            self.active_file = fname



class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(400, 300)

        main_menu = Main_menu(['_File', '_Render', '_Ayuda'])
        main_menu.add_items_to('_File', [
                    ('_Open .pov file...', self.on_open_pov_file),
                    ('_Save .pov file as...', self.on_save_pov_as_file),
                    ('_Quit', self.on_quit_activated)])
        main_menu.add_items_to('_Render', [
                    ('_Render pov file...', self.on_render_pov_file),
                    ('Render with POV-ray', self.on_render_with_pov)])

        self.pov_editor = Pov_editor()

        vbox = Gtk.VBox()
        vbox.pack_start(main_menu, False, False, 0)
        vbox.pack_start(self.pov_editor, True, True, 0)

        self.add(vbox)
        self.show_all()


    def on_quit_activated(self, _):
        Gtk.main_quit()


    def on_open_pov_file(self, _):
        """ Abrir (leer) un archivo .POV. El trabajo se hace en la función
            compartida en 'open_file' (aux.py)
        """
        open_file(Gtk.FileChooserAction.OPEN,
                    self.pov_editor.load_file,
                    (('*.pov', '.POV files (*.pov)'),
                     ('*', 'All files (*)')),
                     initial = 'scenes/' )


    def on_save_pov_as_file(self, _):
        """ Guardar un archivo .POV. El trabajo se hace en la función
            compartida en 'open_file' (aux.py)
        """
        open_file(Gtk.FileChooserAction.SAVE,
                    self.pov_editor.save_file_as,
                    (('*.pov', '.POV files (*.pov)'),
                     ('*', 'All files (*)')),
                     initial = 'scenes/' )


    def on_render_pov_file(self, _):
        """ Renderizar la imagen que corresponde al estado actual editor.
        """
        src = self.pov_editor.get_text()
        elements = parser(src).as_list()

        catalog = {
            'cameras': [],
            'lights':  [],
            'things':  []
        }

        for el in elements:
            key = el[0]
            if key.startswith('#'):             # Es directiva?
                continue
            elif key == 'light_source':
                catalog['lights'].append(Light(el[1:]))

            elif key == 'camera':
                catalog['cameras'].append(Camera(el[1:]))

            elif key == 'sphere':
                catalog['things'].append(Sphere(el[1:]))

            elif key == 'box':
                catalog['things'].append(Box(el[1:]))
                
            elif key == 'cylinder':
                catalog['things'].append(Cylinder(el[1:]))

            else:                               # Es un elemento desconocido!
                print('Pánico...')
                exit(1)

        tracer(WIDTH, HEIGHT, catalog)


    def print_catalog(self, catalog):
        for cat in ['things', 'lights', 'cameras']:
            print(f'Category: {cat}')
            for el in catalog[cat]:
                print('    ', el)


    def on_render_with_pov(self, _):
        """ Renderizar la imagen que corresponde al estado actual editor,
            utilizando el renderizador externo POVray.
        """
        src = self.pov_editor.get_text()
        with open('temp.pov', 'w') as povf:
            povf.write(src)
        cmd = f'povray +P +W{WIDTH} +H{HEIGHT} temp.pov'
        sp.run(cmd.split())


    def run(self):
        Gtk.main()



def main(args):
    mainwdw = MainWindow()
    mainwdw.set_size_request(800, 600)
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
