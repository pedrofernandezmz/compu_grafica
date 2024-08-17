#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  modeller.py
#
#	Alumnos: 
#	~ Valentino Gaggio
#		Clave: 2113503
#		Email: 2113503@ucc.edu.ar
#	~ Agustin Glaiel
#		Clave: 1912095
#		Email: 1912095@ucc.edu.ar
#	~ Pedro Fernández Márquez
#		Clave: 2009636
#		Email: 2009636@ucc.edu.ar
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
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

from aux import warning
from pdb import set_trace as st

ICON_PATH           = 'icons/dark/'     # Ojo - la '/' final es necesaria
MARKER_WIDTH        = 8                 # pixeles
MARKER_HEIGHT       = 8                 # pixeles
MARKER_BORDER_RGBA  = 0xffff00ff        # Amarillo opaco
MARKER_FILL_RGBA    = 0xffff0080        # Amarillo semi-transparente

"""
 __  __       _
|  \/  | __ _(_)_ __      _ __ ___   ___ _ __  _   _
| |\/| |/ _` | | '_ \    | '_ ` _ \ / _ \ '_ \| | | |
| |  | | (_| | | | | |   | | | | | |  __/ | | | |_| |
|_|  |_|\__,_|_|_| |_|___|_| |_| |_|\___|_| |_|\__,_|
                    |_____|
"""

class Main_menu(Gtk.MenuBar):
    """ Esta clase crea un menu, con la siguiente filosofia:
            - Los items principales (File, Edit, etc) se crean en el momento
              de la instanciacion
            - Las aread de programa que desean agregar items a los items
              principales, lo pueden agregar posteriormente.
        El constructor espera una lista de los items principales.
        El metodo 'add_items_to' agrega sub-items a los item principal mediante
        una lista de tuplas
            - Si el primer elemento es None, se 'fabrica' un item separador
            - Caso contrario, se espera el nombre del item, y un 'handler'
              que se ejecutara.
    """
    def __init__(self, items = []):
        super(Main_menu, self).__init__()
        self.main_menu = {}

        for item in items:
            mitem = Gtk.MenuItem(
                        label = item,
                        use_underline = True)
            self.main_menu[item] = Gtk.Menu()
            mitem.set_submenu(self.main_menu[item])
            self.add(mitem)


    def add_items_to(self, main_item, items):
        for item, handler in reversed(items):
            if item == None:
                it = Gtk.SeparatorMenuItem()
            else:
                it = Gtk.ImageMenuItem(
                            label = item,
                            use_underline = True)
                it.connect("activate", handler)

            self.main_menu[main_item].insert(it, 0)


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


class Drawing_canvas(GooCanvas.Canvas):
    def __init__(self):
        super().__init__()

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
    def __init__(self, layer):
        """ El único parámetro de entrada: La capa para dibujar.
        """
        self.layer = layer
        self.id = None

        self.reinit()


    def reinit(self):
        self.markers = []
        self.state = 0


    def in_use(self):
        return len(self.markers) > 0


    def __str__(self):
        inuse = 'in use' if self.in_use() else 'not in use'
        return (f'id: {self.id} ({__class__.__name__} {inuse})')


    def next_state(self, x, y, z, cb):
        print(f'Adding marker {len(self.markers)}, {x:.8g}, {y:.8g} {cb}')
        marker = Marker(self.layer, x, y, z, cb)
        self.markers.append(marker)

"""
 ____
| __ )  _____  __
|  _ \ / _ \ \/ /
| |_) | (_) >  <
|____/ \___/_/\_\

"""

class Box(Thing):
    """ El "box" está definido por dos vértices opuestos.
    """
    def __init__(self, layer):
        """ En el constructor recibimos la capa en la cual dibujar
        """
        super().__init__(layer)


    def add_marker(self, x, y, z):
        """ Agregar marcadores a la forma actual.
            Este método devuelve True si tiene suficiente marcadores
        """
        if not self.in_use():
            self.path = GooCanvas.CanvasPath(
                        parent = self.layer,
                        data = '',
                        width = 0, height = 0,
                        line_width = 2,
                        stroke_color = 'White')

        super().next_state(x, y, z, self.callback)
        if len(self.markers) == 2:
            self.update_path()
            self.generate_pov_code()  # Generar y mostrar el código POV-Ray
            return True
            
    def generate_pov_code(self):
        code = self.to_pov_string()
        print("Código POV-Ray generado:")
        print(code)


    def to_pov_string(self):
        x0, y0 = self.markers[0].get_pos()
        x1, y1 = self.markers[1].get_pos()
        return (f'box {{\n'
                f'    <{x0}, {y0}, 0> <{x1}, {y1}, 0>\n'
                f'}}\n\n')


    def update_path(self):
        x0, y0 = self.markers[0].get_pos()
        x1, y1 = self.markers[1].get_pos()
        data = f'M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} z'
        self.path.set_property('data', data)


    def callback(self, x, y):
        self.update_path()

"""
 ____        _
/ ___| _ __ | |__   ___ _ __ ___
\___ \| '_ \| '_ \ / _ \ '__/ _ \
 ___) | |_) | | | |  __/ | |  __/
|____/| .__/|_| |_|\___|_|  \___|
      |_|
"""
class Sphere(Thing):
    """ El "Sphere" está definido por dos vértices uno determina el centro y el otro el radio.
    """
    def __init__(self, layer):
        """ En el constructor recibimos la capa en la cual dibujar
        """
        super().__init__(layer)
        self.radius = 1  # Radio igual a 1 para dibujar menor da error...

    def add_marker(self, x, y, z):
        """ Agregar marcadores a la forma actual.
            Este método devuelve True si tiene suficientes marcadores
        """
        if not self.in_use():
            self.path = GooCanvas.CanvasEllipse(
                parent=self.layer,
                center_x=x,
                center_y=y,
                radius_x=self.radius,
                radius_y=self.radius,
                line_width=2,
                stroke_color='Blue' # Color para identificar figura
            ) # Utilizo CanvasEllipse para circulo

        super().next_state(x, y, z, self.callback)
        if len(self.markers) == 2:
            self.update_path()
            self.generate_pov_code()  # Generar y mostrar el código POV-Ray
            return True
            
    def generate_pov_code(self):
        code = self.to_pov_string()
        print("Código POV-Ray generado:")
        print(code)

    def to_pov_string(self):
        cx, cy = self.markers[0].get_pos()
        return (
            f'sphere {{\n'
            f'    <{cx}, {cy}, 0>, {self.radius}\n'
            f'}}\n\n'
        )

    def update_path(self):
        cx, cy = self.markers[0].get_pos()
        x, y = self.markers[1].get_pos()
        self.radius = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5  # Calculo el nuevo radio al mover marcador
        self.path.set_property('center-x', cx)
        self.path.set_property('center-y', cy)
        self.path.set_property('radius-x', self.radius)
        self.path.set_property('radius-y', self.radius)

    def callback(self, x, y):
        self.update_path()

"""
  ____
 / ___|___  _ __   ___
| |   / _ \| '_ \ / _ \
| |__| (_) | | | |  __/
 \____\___/|_| |_|\___|

"""

"""
  ____      _ _           _
 / ___|   _| (_)_ __   __| | ___ _ __
| |  | | | | | | '_ \ / _` |/ _ \ '__|
| |__| |_| | | | | | | (_| |  __/ |
 \____\__, |_|_|_| |_|\__,_|\___|_|
      |___/
"""
class Cylinder(Thing):
    """ El "cylinder" está definido por dos vértices opuestos.
    """
    def __init__(self, layer):
        """ En el constructor recibimos la capa en la cual dibujar
        """
        super().__init__(layer)

    def add_marker(self, x, y, z):
        """ Agregar marcadores a la forma actual.
            Este método devuelve True si tiene suficientes marcadores
        """
        if not self.in_use():
            self.path = GooCanvas.CanvasPath(
                        parent = self.layer,
                        data = '',
                        width = 0, height = 0,
                        line_width = 2,
                        stroke_color = 'Green') # Color para identificar figura

        super().next_state(x, y, z, self.callback)
        if len(self.markers) == 2:
            self.update_path()
            self.generate_pov_code()  # Generar y mostrar el código POV-Ray
            return True
            
    def generate_pov_code(self):
        code = self.to_pov_string()
        print("Código POV-Ray generado:")
        print(code)

    def to_pov_string(self):
        x0, y0 = self.markers[0].get_pos()
        x1, y1 = self.markers[1].get_pos()
        diameter = abs(x1 - x0) # Calculo diametro y altura valor absoluto de la diferencia
        height = abs(y1 - y0)
        return (f'cylinder {{\n'
                f'    <{x0}, {y0}, 0>, <{x0}, {y0}, {height}>, {diameter/2}\n'
                f'}}\n\n')

    def update_path(self):
        x0, y0 = self.markers[0].get_pos()
        x1, y1 = self.markers[1].get_pos()
        data = f'M{x0},{y0} L{x1},{y0} L{x1},{y1} L{x0},{y1} z'
        self.path.set_property('data', data)

    def callback(self, x, y):
        self.update_path()

"""
 _____
|_   _|__  _ __ _   _ ___
  | |/ _ \| '__| | | / __|
  | | (_) | |  | |_| \__ \
  |_|\___/|_|   \__,_|___/

"""

"""
 ____       _
|  _ \ _ __(_)___ _ __ ___
| |_) | '__| / __| '_ ` _ \
|  __/| |  | \__ \ | | | | |
|_|   |_|  |_|___/_| |_| |_|

"""

"""
 ____       _
|  _ \ ___ | |_   _  __ _  ___  _ __
| |_) / _ \| | | | |/ _` |/ _ \| '_ \
|  __/ (_) | | |_| | (_| | (_) | | | |
|_|   \___/|_|\__, |\__, |\___/|_| |_|
              |___/ |___/
"""

"""
 _____     _                   _
|_   _| __(_) __ _ _ __   __ _| | ___
  | || '__| |/ _` | '_ \ / _` | |/ _ \
  | || |  | | (_| | | | | (_| | |  __/
  |_||_|  |_|\__,_|_| |_|\__, |_|\___|
                         |___/
"""

"""
 ____  _
|  _ \| | __ _ _ __   ___
| |_) | |/ _` | '_ \ / _ \
|  __/| | (_| | | | |  __/
|_|   |_|\__,_|_| |_|\___|

"""

"""
 _____         _
|_   _|____  _| |_
  | |/ _ \ \/ / __|
  | |  __/>  <| |_
  |_|\___/_/\_\\__|

"""

"""
  ____
 / ___|__ _ _ __ ___   ___ _ __ __ _
| |   / _` | '_ ` _ \ / _ \ '__/ _` |
| |__| (_| | | | | | |  __/ | | (_| |
 \____\__,_|_| |_| |_|\___|_|  \__,_|

"""

"""
 ____                     _                               _   _
|  _ \ _ __ __ ___      _(_)_ __   __ _     ___  ___  ___| |_(_) ___  _ __
| | | | '__/ _` \ \ /\ / / | '_ \ / _` |   / __|/ _ \/ __| __| |/ _ \| '_ \
| |_| | | | (_| |\ V  V /| | | | | (_| |   \__ \  __/ (__| |_| | (_) | | | |
|____/|_|  \__,_| \_/\_/ |_|_| |_|\__, |___|___/\___|\___|\__|_|\___/|_| |_|
                                  |___/_____|
"""

class Drawing_section(Gtk.Frame):
    def __init__(self, top):
        """ Creación de la parte gráfica.
        """
        super().__init__(label = 'Dibujo')

        # Todo se organizará dentro de una Gtk.Grid
        self.draw_grid = Gtk.Grid(margin = 4)
        self.add(self.draw_grid)

        # Esta es la lista de elementos para la barra de herramientas
        # Es un diccionario, y el valor de cada entrada contiene una lista
        # de parámetros. El primer parámetros es la clase a inicializa corres-
        # pondiente. (después se agregarán probablemente mas parámetros)
        # None indica que la clase aún no está implementada.
        self.icons = {'pointer':    [None],
                      'box':        [Box],
                      'sphere':     [Sphere],
                      'cone':       [None],
                      'cylinder':   [Cylinder],
                      'torus':      [None],
                      'prism':      [None],
                      'polygon':    [None],
                      'triangle':   [None],
                      'plane':      [None],
                      'text':       [None],
                      'light':      [None],
                      'camera':     [None]}

        self.selected_tool = None
        self.selected_icon = None

        hbox = Gtk.HBox(spacing = 3, hexpand = True)
        self.draw_grid.attach(hbox, 0, 0, 1, 1)

        # Crear los botones para selección de figuras
        for icon in self.icons:
            btn = Gtk.Button()
            img = Gtk.Image.new_from_file(ICON_PATH + icon + ".svg")
            btn.set_image(img)
            btn.set_tooltip_text(icon)
            btn.connect('clicked', self.on_tool_selected, icon)
            hbox.pack_start(btn, False, False, 0)

        # Esta imagen será el indicador de 'herramienta seleccionada'.
        self.selected_img = Gtk.Image()
        hbox.pack_end(self.selected_img, False, False, 0)

        # La superficie de dibujo
        scroller = Gtk.ScrolledWindow(vexpand = True)
        self.draw_canvas = Drawing_canvas()
        self.draw_cvroot = self.draw_canvas.get_root_item()
        self.draw_grid.attach(scroller, 0, 1, 1, 1)
        scroller.add(self.draw_canvas)
        self.draw_cvroot.connect(
                    'button-press-event', self.on_canvas_button_press)


    def on_canvas_button_press(self, src, tgt, event):
        """ Cuando se oprime el botón 1 (izquierda), se iniciará la figura
        """
        # Botón 1 (izquierda)?
        if event.button == 1:
            if self.selected_tool:
                done = self.selected_tool.add_marker(event.x, event.y, 0)
                if done:
                    icon = self.selected_icon
                    self.selected_tool = self.icons[icon][0](self.draw_cvroot)

        elif event.button == 2:
            pass


    def on_tool_selected(self, btn, icon):
        """ Cambio de herramienta:
                - Si la herramienta actual tiene marcadores:
                    Pedir confirmación antes de descartar
        """

        if self.icons[icon][0]:         # hay código definido?
            self.selected_img.set_from_pixbuf(btn.get_image().get_pixbuf())

            if self.selected_tool:
                # Si hay una herramienta seleccionada anteriormente, deselecciónala
            	self.selected_tool = None

            self.selected_icon = icon
            self.selected_tool = self.icons[icon][0](self.draw_cvroot)

        else:
            self.selected_img.clear()
            self.selected_tool = None
            warning('No implementado', 'Aún no tiene código')


"""
  ____                      _                        _   _
 / ___|___  _ __  ___  ___ | | ___     ___  ___  ___| |_(_) ___  _ __
| |   / _ \| '_ \/ __|/ _ \| |/ _ \   / __|/ _ \/ __| __| |/ _ \| '_ \
| |__| (_) | | | \__ \ (_) | |  __/   \__ \  __/ (__| |_| | (_) | | | |
 \____\___/|_| |_|___/\___/|_|\___|___|___/\___|\___|\__|_|\___/|_| |_|
                                 |_____|
"""
class Console_section(Gtk.Frame):
    def __init__(self, top):
        super().__init__(label = 'Consola')
        self.console_grid = Gtk.Grid()
        self.add(self.console_grid)

"""
 __  __       _    __        ___           _
|  \/  | __ _(_)_ _\ \      / (_)_ __   __| | _____      __
| |\/| |/ _` | | '_ \ \ /\ / /| | '_ \ / _` |/ _ \ \ /\ / /
| |  | | (_| | | | | \ V  V / | | | | | (_| | (_) \ V  V /
|_|  |_|\__,_|_|_| |_|\_/\_/  |_|_| |_|\__,_|\___/ \_/\_/

"""
class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(1000, 700)

        top_vbox = Gtk.VBox()

        main_menu = Main_menu(['_Archivo', 'A_yuda'])
        main_menu.add_items_to('A_yuda', [
                    ('_Acerca', self.on_about_activated)])
        top_vbox.pack_start(main_menu, False, False, 0)

        top_hbox = Gtk.HBox(margin = 4, spacing = 6)
        top_vbox.pack_start(top_hbox, True, True, 0)

        drawing = Drawing_section(self)
        top_hbox.pack_start(drawing, True, True, 0)

        console = Console_section(self)
        top_hbox.pack_start(console, False, False, 0)

        self.add(top_vbox)
        self.show_all()


    def on_about_activated(self, menuitem):
        dlg = Gtk.AboutDialog(
                    authors = ['John Coppens']
        )
        dlg.run()
        dlg.destroy()


    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
