#! /usr/bin/env python

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import os
from mothmusicplayer3 import mediaInfo2
from mothmusicplayer3 import configuration


class filechooser:
    media_ = mediaInfo2.mediaTag()

    def __init__(self, playlist, playlist_class):
        self.playlist = playlist
        self.store = playlist_class.store
        self.playlist_class_ = playlist_class
        self.sel_array = [[''], ['']]
        self.count = 0

        self.file_filter = Gtk.FileFilter()
        self.file_filter.set_name("Audio")
        self.file_filter.add_mime_type("audio/mpeg")
        self.file_filter.add_mime_type("audio/ogg")
        self.file_filter.add_pattern("*.mp3")
        self.file_filter.add_pattern("*.flac")
        self.file_ = None
        self.all_filter = Gtk.FileFilter()
        self.all_filter.set_name("Everything")
        self.all_filter.add_pattern("*")

        self.folder = configuration.get_conf("file_chooser", "default_load_path", "string")

    def on_key_press_event(self, widget, event, flag=0):
        if not flag:
            keyname = Gdk.keyval_name(event.keyval)
        else:
            keyname = ""

        print(keyname)

        if keyname == "Shift_L" or keyname == "Shift_R" or flag:
            if flag:
                items = self.sel_array[(self.count) % 2]
            else:
                items = widget.get_filenames()

            # print items
            for item in items:
                if os.path.isfile(item):
                    x = self.store
                    n = len(x)
                    if n < 0:
                        n = 0
                    self.store.append([n, self.media_.track_get_title(item), self.media_.track_get_artist(item),
                                       self.media_.track_get_album(item), "#000000", item, ""])
                    self.playlist_class_.index_update()
                    self.playlist.put_item_into_playlist(self.playlist.internal_playlist, item)
                if os.path.isdir(item):
                    items_in_dir = os.listdir(item)
                    for item_ in items_in_dir:
                        ending = item_.split(".")[-1]
                        if not (ending == "mp3" or ending == "flac"):
                            continue
                        item_ = item + "/" + item_
                        if os.path.isfile(item_):
                            x = self.store
                            n = len(x)
                            if n < 0:
                                n = 0
                            self.store.append(
                                [n, self.media_.track_get_title(item_), self.media_.track_get_artist(item_),
                                 self.media_.track_get_album(item_), "#000000", item, ""])
                            self.playlist_class_.index_update()
                            self.playlist.put_item_into_playlist(self.playlist.internal_playlist, item_)


    def file_chooser_places_show_hide(self):
        file_box = self.file_.get_children()[0].get_children()[1].get_children()[0]  # .get_children()[1]
        if configuration.get_conf("file_chooser", "show_places"):
            file_box.show()
        else:
            file_box.hide()

    def selection_changed(self, a, widget):
        items = widget.get_filenames()
        self.sel_array[self.count] = items
        self.count = (self.count + 1) % 2

    def current_folder_changed(self, file):
        current_folder_uri = file.get_current_folder_uri()
        model.prepend()
        iter = model.get_iter_root()
        model.set(iter,"SAADAd")
        print("blalbal")

    def file_chooser_box2(self):
        box = Gtk.HBox(False, 0)
        file_ = Gtk.FileChooserWidget()

        file_.add_filter(self.file_filter)
        file_.add_filter(self.all_filter)
        file_.set_filter(self.file_filter)

        file_.set_action(Gtk.FileChooserAction.OPEN)
        # implement a check here!!
        file_.set_current_folder(configuration.get_conf("file_chooser", "default_load_path", "string"))
        file_.set_show_hidden(False)
        file_.set_select_multiple(True)
        file_.set_property("has-focus", False)

        #used for the enter key hacks
        file_tree = \
        file_.get_children()[0].get_children()[1].get_children()[1].get_children()[0].get_children()[0].get_children()[
            0]  #.get_children()[0]
        #file_tree.hide()
        file_tree_selection = file_tree.get_selection()
        file_tree_selection.connect("changed", self.selection_changed, file_)


        file_.connect("key-press-event", self.on_key_press_event, 0)
        file_.connect("file-activated", self.on_key_press_event, None, 1)
        file_.connect("current-folder-changed", self.current_folder_changed)

        self.file_ = file_
        self.file_chooser_places_show_hide()

        box.pack_start(file_, True, True, 0)

        file_.show()
        box.show()
        return box
