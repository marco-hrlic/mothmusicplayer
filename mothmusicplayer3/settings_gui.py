#! usr/bin/env python

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mothmusicplayer3 import configuration


class preferences_gui:
    def show_settings_window(self):
        # reinitialize the window
        self.__init__(self.parent)
        self.settings_window.show()
        self.is_shown = True

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        self.settings_window.destroy()
        self.is_shown = False

    def __init__(self, parent):
        self.settings_window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.settings_window.set_title("Settings")
        self.settings_window.set_default_size(512, 512)
        # self.window.set_icon_from_file("icon.png")
        self.settings_window.connect("destroy", self.destroy)

        self.is_shown = False
        self.parent = parent
        scroll_window = Gtk.ScrolledWindow()
        scroll_window.grab_focus()
        scroll_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroll_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.store = self.create_store()
        self.treeView = Gtk.TreeView(self.store)
        self.treeView.set_rules_hint(True)
        self.treeView.set_enable_search(True)

        self.player = self.parent.parent.player

        self.playlist_create_columns(self.treeView)

        scroll_window.add(self.treeView)
        self.settings_window.add(scroll_window)

        scroll_window.show()
        self.treeView.show()


        #

    # /NEEDS TO BE CHANGED!!!!!!
    #
    def create_store(self):
        store = Gtk.TreeStore(str, str)
        data_sections = configuration.get_sections()
        for section in data_sections:
            piter = store.append(None, [section, ""])
            for option in configuration.get_options(section):
                store.append(piter, [option, str(configuration.get_conf(section, option, "string"))])
        return store

    def playlist_create_columns(self, treeView):
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Property", rendererText, text=0)
        column.set_sort_column_id(0)
        treeView.append_column(column)

        rendererText = Gtk.CellRendererText()
        rendererText.set_property('editable', True)
        rendererText.connect("edited", self.cell_toggled)
        column = Gtk.TreeViewColumn("Value", rendererText, text=1)
        column.set_sort_column_id(1)
        treeView.append_column(column)

    def get_keybinder(self, binder=None):
        self.binder = binder

    def cell_toggled(self, cell, path, text):
        iterator = self.store.get_iter(path)
        section = self.store.get(self.store.iter_parent(iterator), 0)[0]
        option = self.store.get(iterator, 0)[0]
        self.store.set_value(iterator, 1, text)
        configuration.set_conf(section, option, text)
        if section == "keybindings":
            self.binder.get_keybindings()
            self.binder.bind_keys()
        if option == "show_places":
            self.parent.parent.file_chooser__.file_chooser_places_show_hide()
        if section == "eq":
            self.player.eq_set(int(option[4]), int(text))
        if option == "show_console":
            self.parent.parent.console.show_hide()
        if option == "show_infobar":
            self.parent.parent.infobar.show_hide()

    def playlist_create_model(self):
        '''create the model - a ListStore'''
        data = configuration.get_sections()
        store = Gtk.ListStore(str, int)
        for item in data:
            store.append([item, 0])
        return store
        


