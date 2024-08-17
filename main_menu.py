#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


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
