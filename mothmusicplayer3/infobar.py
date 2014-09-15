#!/usr/bin/env python
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mothmusicplayer3 import mediaInfo2
from mothmusicplayer3 import configuration


class infobar:
    media = mediaInfo2.mediaTag()

    def __init__(self, parent):
        self.parent = parent
        self.infotext_artist = ""
        self.infotext_title = ""
        self.infotext_album = ""

    def current_index(self):
        return self.parent.player.current_track_playlist_index

    def update(self):
        data = self.parent.playlist__.store[self.current_index() - 1]
        self.infotext_artist = data[2]
        self.infotext_title = data[1]
        self.infotext_album = data[3]
        # self.label.set_text("..::    "+ self.infotext_title + "  -  " + self.infotext_artist + "  -  " + self.infotext_album + "    ::..")
        self.label.set_markup(
            "<span weight = \"light\"> " + "..::    " + self.infotext_title + "  -  " + self.infotext_artist + "  -  " + self.infotext_album + "    ::.." + "</span>")

    def show_hide(self):
        state = configuration.get_conf("player", "show_infobar", "bool")
        if state:
            self.box.show()
        else:
            self.box.hide()

    def infobar_gui(self):
        self.box = Gtk.HBox(True)
        self.label = Gtk.Label()
        self.box.pack_start(self.label, False, False, 0)
        self.show_hide()
        self.label.show()
        return self.box

        
