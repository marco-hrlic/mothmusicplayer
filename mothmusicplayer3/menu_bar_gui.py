#! usr/bin/env python2

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class menu_bar_:
    def menu_bar(self):
        box = Gtk.HBox(False, 5)

        self.file_menu = Gtk.Menu()

        self.open_item = Gtk.MenuItem("Open")
        self.save_item = Gtk.MenuItem("Save")
        self.quit_item = Gtk.MenuItem("Quit")

        self.file_menu.append(self.open_item)
        self.file_menu.append(self.save_item)
        self.file_menu.append(self.quit_item)

        self.open_item.show()
        self.save_item.show()
        self.quit_item.show()

        self.menu_bar = Gtk.MenuBar()
        self.menu_bar.show()

        self.file_item = Gtk.MenuItem("File")
        self.file_item.set_submenu(self.file_menu)
        self.menu_bar.append(self.file_item)

        self.file_item.show()

        box.pack_start(self.menu_bar, True, True, 0)
        box.show()
        return box
