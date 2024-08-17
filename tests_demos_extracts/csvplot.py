#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  csvplot.py
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

from main_menu import Main_menu
from aux import warning

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import Gtk, GooCanvas

import csv

SCALE = 25

class Plotter(Gtk.ScrolledWindow):
    def __init__(self):
        super().__init__(hexpand = True, vexpand = True)
        self.headers = None
        self.data = []

        self.canvas = GooCanvas.Canvas(
                    automatic_bounds = True,
                    bounds_from_origin = False)
        self.cvroot = self.canvas.get_root_item()

        org_layer = GooCanvas.CanvasGroup(parent = self.cvroot)
        self.plot_layer = GooCanvas.CanvasGroup(parent = self.cvroot)

        # Origin
        lines = GooCanvas.CanvasPoints.new(2)
        lines.set_point(0, -25, 0)
        lines.set_point(1,  25, 0)
        GooCanvas.CanvasPath(parent = org_layer,
                    data = 'm0 -50 l0 100 m0 -50',
                    line_width = 2,
                    stroke_color = 'Yellow')

        lines.set_point(0, 0, -25)
        lines.set_point(1, 0,  25)
        GooCanvas.CanvasPath(parent = org_layer,
                    data = 'm-50 0 l100 0 m-50 0',
                    line_width = 2,
                    stroke_color = 'Yellow')

        self.add(self.canvas)


    def load_csv(self, fname):
        self.clear()
        with open(fname, 'r') as inf:
            rdr = csv.reader(inf)

            self.headers = next(rdr, None)
            print(self.headers)
            for row in rdr:
                if len(row) != len(self.headers):
                    continue
                self.data.append([float(r) for r in row])


    def plot(self, ycol, xcol):
        for row in self.data:
            print(row[ycol], row[xcol])
            GooCanvas.CanvasRect(
                        parent = self.plot_layer,
                        x = row[ycol]*SCALE, y = -row[xcol]*SCALE,
                        width = 1, height = 1,
                        line_width = 2,
                        stroke_color = 'White')


    def clear(self):
        for i in range(self.plot_layer.get_n_children()):
            self.plot_layer.get_child(0).remove()



class Mode_selector(Gtk.HBox):
    def __init__(self):
        super().__init__(spacing = 4)

        self.store = Gtk.ListStore(str)

        self.pack_start(Gtk.Label(label = 'Plot: '), False, False, 0)
        self.ycol = Gtk.ComboBoxText(model = self.store)
        self.ycol.set_size_request(70, -1)
        self.ycol.set_active(0)
        self.pack_start(self.ycol, False, False, 0)

        self.pack_start(Gtk.Label(label = ' against: '), False, False, 0)
        self.xcol = Gtk.ComboBoxText(model = self.store)
        self.xcol.set_size_request(70, -1)
        self.xcol.set_active(0)
        self.pack_start(self.xcol, False, False, 0)


    def set_options(self, options):
        for el in options:
            self.store.append([el])


    def get_active(self):
        return self.ycol.get_active(), self.xcol.get_active()



class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(1200, 500)

        main_menu = self.make_main_menu()

        self.plotter = Plotter()
        self.csv_status = self.make_csv_status()
        self.mode_sel = Mode_selector()

        self.mode_sel.pack_start(Gtk.Label(label = '  x: '), False, False, 0)
        self.x_pos_lbl = Gtk.Label(label = 0.0)
        self.x_pos_lbl.set_size_request(50, -1)
        self.mode_sel.pack_start(self.x_pos_lbl, False, False, 0)

        self.mode_sel.pack_start(Gtk.Label(label = '  y: '), False, False, 0)
        self.y_pos_lbl = Gtk.Label(label = 0.0)
        self.y_pos_lbl.set_size_request(50, -1)
        self.mode_sel.pack_start(self.y_pos_lbl, False, False, 0)

        run_button = Gtk.Button.new_from_icon_name('system-run', Gtk.IconSize.BUTTON)
        run_button.connect('clicked', self.on_run_plot)
        self.mode_sel.pack_start(run_button, False, False, 0)

        clear_button = Gtk.Button.new_from_icon_name('edit-clear', Gtk.IconSize.BUTTON)
        clear_button.connect('clicked', self.on_clear_plot)
        self.mode_sel.pack_start(clear_button, False, False, 0)

        self.vbox = Gtk.VBox(margin = 5, spacing = 4)
        self.vbox.pack_start(main_menu, False, False, 0)
        self.vbox.pack_start(self.csv_status, False, False, 0)
        self.vbox.pack_start(self.mode_sel, False, False, 0)
        self.vbox.pack_start(self.plotter, True, True, 0)

        self.add(self.vbox)
        self.show_all()


    def on_run_plot(self, button):
        ycol, xcol = self.mode_sel.get_active()
        if (ycol == -1) or (xcol == -1):
            warning('Missing info', 'Select columns to be plotted first!')
            return
        self.plotter.plot(ycol, xcol)


    def on_clear_plot(self, button):
        self.plotter.clear()


    def make_csv_status(self):
        stat = Gtk.HBox()
        lbl1 = Gtk.Label(label = 'CSV-file: ')
        stat.pack_start(lbl1, False, False, 0)
        self.fname = Gtk.Label(label = '')
        self.fname_lbl = Gtk.Label(label = '')
        stat.pack_start(self.fname_lbl, False, False, 0)
        return stat


    def make_main_menu(self):
        menu = Main_menu(['_Files', '_Plot', '_Help'])
        menu.add_items_to('_Files', [
                    [None, None],
                    ['_Quit', self.quit]])
        menu.add_items_to('_Plot', [
                    [None, None],
                    ['_Load CSV file...', self.load_csv]])
        return menu


    def load_csv(self, menuitem):
        fc = Gtk.FileChooserDialog(
                    action = Gtk.FileChooserAction.OPEN)
        fc.add_buttons('Cancel', Gtk.ResponseType.CANCEL,
                       'Open', Gtk.ResponseType.ACCEPT)
        filter = Gtk.FileFilter()
        filter.set_name('CSV files (*.csv)')
        filter.add_pattern('*.csv')
        fc.add_filter(filter)

        if fc.run() == Gtk.ResponseType.ACCEPT:
            fname = fc.get_filename()
            self.fname_lbl.set_text(fname)
            self.plotter.clear()
            self.plotter.load_csv(fname)
            self.mode_sel.set_options(self.plotter.headers)

        fc.destroy()


    def run(self):
        Gtk.main()


    def quit(self, menuitem):
        Gtk.main_quit()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
