#!/usr/bin/env python

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk
import os
from mothmusicplayer3 import mediaInfo2


class playlist_builder:
    media_ = mediaInfo2.mediaTag()

    def __init__(self, parent_class):
        self.parent = parent_class
        self.playlist = self.parent.playlist
        self.player = self.parent.player
        self.timer = self.parent.timer
        self.prev_index = 0
        self.store = self.playlist_create_model()

    def playlist_selection_change(self, index):
        treeiter = self.store.get_iter((index,))
        selection = self.treeView.get_selection()
        selection.select_iter(treeiter)
        path = self.store.get_path(treeiter)
        self.treeView.set_cursor_on_cell(path, None, None, False)
        self.treeView.scroll_to_cell(path, None, False, False, False)
        self.color_update(index)

        self.parent.infobar.update()

    def playlist_create_columns(self, treeView):


        rendererText = Gtk.CellRendererText()
        rendererPixbuf = Gtk.CellRendererPixbuf()
        column = Gtk.TreeViewColumn("Index")
        column.pack_start(rendererText, True)
        column.set_attributes(rendererText, text=0, foreground=4)
        column.pack_start(rendererPixbuf, True)
        column.add_attribute(rendererPixbuf, "stock-id", 6)
        column.set_sort_column_id(0)
        column.set_resizable(False)
        treeView.append_column(column)

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", rendererText, text=1, foreground=4)
        column.set_sort_column_id(1)
        column.set_resizable(True)
        column.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        column.set_expand(True)
        treeView.append_column(column)

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Artist", rendererText, text=2, foreground=4)
        column.set_sort_column_id(2)
        column.set_resizable(True)
        column.set_expand(True)
        treeView.append_column(column)

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Album", rendererText, text=3, foreground=4)
        column.set_sort_column_id(3)
        column.set_resizable(True)
        column.set_expand(True)
        treeView.append_column(column)


    def playlist_create_model(self):
        items = self.playlist.get_items_from_playlist(self.playlist.internal_playlist)
        data = [(int(x), self.media_.track_get_title(item), self.media_.track_get_artist(item),
                 self.media_.track_get_album(item), item) \
                for x, item, in enumerate(items)]
        store = Gtk.ListStore(int, str, str, str, str, str, str)
        for item in data:
            store.append([item[0], item[1], item[2], item[3], "#808080", item[4], ""])
            # 0-index,1-title,2-artist,3-album,4-color,5-path,6-icon
        return store


    def row_activated(self, treeview, path, view_column, store):
        treeiter = store.get_iter(path)
        value = store.get_value(treeiter, 0)
        if self.player.current_track_playlist_index != value + 1:

            if self.player.current_track_playlist_index < 0:
                self.player.current_track_playlist_index = 1

            if self.player.is_playing:
                self.player.stop_track()
            if self.timer != None:
                GObject.source_remove(self.timer)
            self.player.load_track_from_playlist(self.playlist.playlist, value + 1)
            self.player.start_track()
            self.timer = GObject.timeout_add(1000, self.parent.player_controls__.seek_bar__.update_time_label)
            self.color_update(path[0])

    def remove_selected(self, menu, treeView):
        selection = treeView.get_selection()
        paths = selection.get_selected_rows()[1]
        for path in reversed(paths):
            index = path[0]
            treeiter = self.store.get_iter(path)
            # for x in path:
            #    print x
            self.playlist.delete_item_by_number(self.playlist.playlist, index + 1)
            self.store.remove(treeiter)
            self.player.index_change(index + 1)
            if (index < self.prev_index):
                self.prev_index = self.prev_index - 1
        self.index_update()

    def update_queue(self):
        for index in range(0, len(self.store)):
            if index in list(self.parent.player.track_queue.queue):
                self.store[index][6] = Gtk.STOCK_APPLY
            elif not self.store[index][6] == Gtk.STOCK_MEDIA_PLAY:
                self.store[index][6] = ""

    def color_update(self, index):
        self.store[self.prev_index][4] = "#808080"
        self.store[self.prev_index][6] = ""
        self.store[index][4] = "#2A62C9"
        self.store[index][6] = Gtk.STOCK_MEDIA_PLAY
        self.prev_index = index
        self.update_queue()

    def index_update(self):
        counter = 0;
        for item in self.store:
            item[0] = counter;
            counter = counter + 1

    def select_all(self, menu, treeView):
        treeView.get_selection().select_all()

    def right_click(self, treeView, event):
        if event.button == 3:
            menu = Gtk.Menu()
            menu_item_delete = Gtk.MenuItem("Delete")
            menu_item_select_all = Gtk.MenuItem("Select all")
            menu.append(menu_item_delete)
            menu.append(menu_item_select_all)
            menu_item_delete.connect("activate", self.remove_selected, treeView)
            menu_item_select_all.connect("activate", self.select_all, treeView)
            menu_item_delete.show()
            menu_item_select_all.show()
            menu.popup(None, None, None, event.button, event.time)

    def keypress(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "BackSpace":
            self.remove_selected(None, widget)

    def drop(self, widget, context, x, y, time):
        # simulate a key press in file chooser
        self.parent.file_chooser__.on_key_press_event(None, None, 1)
        context.finish(True, False, time)

    def motion(self, widget, context, x, y, time):
        # context.drag_status(Gdk.DragAction.COPY, time)
        return True

    def playlist_box(self):
        box = Gtk.VBox(False)
        self.box_ref = box

        scroll_window = Gtk.ScrolledWindow()
        # scroll_window.set_flags(Gtk.CAN_FOCUS)
        scroll_window.grab_focus()
        scroll_window.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
        scroll_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(scroll_window, True, True, 0)

        scroll_window.drag_dest_set(0, [], 0)
        scroll_window.connect("drag_drop", self.drop)
        scroll_window.connect("drag_motion", self.motion)
        self.treeView = Gtk.TreeView(self.store)
        self.treeView.set_rules_hint(True)
        self.treeView.set_enable_search(True)
        self.treeView.set_search_equal_func(self.search_func, None)
        self.treeView.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

        self.treeView.connect("row-activated", self.row_activated, self.store)
        self.treeView.connect("button-press-event", self.right_click)

        self.treeView.connect("key-press-event", self.keypress)

        scroll_window.add(self.treeView)
        self.playlist_create_columns(self.treeView)

        #self.enter_playlist_edit_mode()

        scroll_window.show()
        self.treeView.show()
        box.show()

        return box

    def search_func(self, model, column, key, iterator, data=None):
        value0 = model.get_value(iterator, 0)
        value1 = model.get_value(iterator, 1)
        value2 = model.get_value(iterator, 2)
        value = str(value0) + value1 + value2
        if str(key).lower() in str(value).lower():
            return False
        return True

    def enter_playlist_edit_mode(self):
        self.treeView.get_selection().set_mode(Gtk.SelectionMode.MULTIPLE)

    def exit_playlist_edit_mode(self):
        self.treeView.get_selection().set_mode(Gtk.SelectionMode.SINGLE)
