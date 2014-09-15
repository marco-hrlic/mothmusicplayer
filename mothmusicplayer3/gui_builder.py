#!/usr/bin/env python
import gi
from gi.repository import Gtk, GObject, Gdk
gi.require_version('Gtk', '3.0')
import os
from mothmusicplayer3 import mediaInfo2
from mothmusicplayer3 import configuration
from mothmusicplayer3 import playlist_gui
from mothmusicplayer3 import filechooser_gui
from mothmusicplayer3 import menu_bar_gui
from mothmusicplayer3 import player_controls_gui
from mothmusicplayer3 import console
from mothmusicplayer3 import infobar


class main_window:
    media_ = mediaInfo2.mediaTag()

    def file_path(self):
        return os.path.split(os.path.abspath(__file__))[0] + '/icon.png'


    def __init__(self, player, playlist):
        self.duration = None
        self.player = player
        self.playlist = playlist
        self.timer = None
        self.default_layout()
        self.is_seeking = False
        self.percent = 0
        self.prev_index = 0
        GObject.threads_init()
        self.explorer = True
        self.folder = ""

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        print("destroy")
        if bool(configuration.get_conf("player", "empty_playlist_on_close")):
            self.playlist.empty_playlist(os.path.abspath(os.getcwd() + '/' + self.playlist.playlist))
        self.player.exit_player()
        self.player_controls.settings.destroy()
        Gtk.main_quit()

    def default_layout(self):

        # main_window
        self.window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        self.window.set_title("Moth Music Player")
        self.window.set_default_size(1024, 512)
        self.window.set_icon_from_file(self.file_path())

        self.window.connect("destroy", self.destroy)
        self.window.connect("key_press_event", self.key_press)

        self.box1 = Gtk.VBox(False, 0)
        self.box2 = Gtk.HPaned()
        self.box2.set_position(self.window.get_size()[0] / 2)
        self.box3 = Gtk.HBox(False, 10)
        self.box4 = Gtk.VBox(False, 0)

        self.window.add(self.box1)

        self.menu = menu_bar_gui.menu_bar_().menu_bar()

        self.player_controls__ = player_controls_gui.player_controls_(self)
        self.player_controls_ = self.player_controls__.player_controls()

        self.playlist__ = playlist_gui.playlist_builder(self)
        self.playlist_ = self.playlist__.playlist_box()

        self.file_chooser__ = filechooser_gui.filechooser(self.playlist, self.playlist__)
        self.file_chooser_ = self.file_chooser__.file_chooser_box2()

        self.file_box = Gtk.HBox(False, 0)
        self.file_box.pack_start(self.file_chooser_, True, True, 0)

        self.console = console.console(self)
        self.console_box = Gtk.HBox(False, 0)
        self.console_box = self.console.console_gui()

        self.infobar = infobar.infobar(self)
        self.infobar_box = Gtk.HBox(False, 0)
        self.infobar_box = self.infobar.infobar_gui()

        self.box1.pack_start(self.player_controls_, False, False, 0)
        self.box1.pack_start(self.infobar_box, False, False, 0)
        self.box3.pack_start(self.box2, True, True, 5)
        self.box1.pack_start(self.box3, True, True, 5)
        self.box2.add1(self.file_box)
        self.box1.pack_start(self.console_box, False, False, 0)
        self.box2.add2(self.playlist_)

        self.player_controls__.connect_handlers()

        self.box1.show()
        self.box2.show()
        self.box3.show()
        self.box4.show()
        self.window.show()
        self.show_hide_filechooser()
        self.playlist__.treeView.grab_focus()

    def key_press(self, widget, data=None):
        keyname = Gdk.keyval_name(data.keyval)
        if keyname == "colon":
            self.console.show_hide(True)
            self.console.textbox.grab_focus()

    def show_hide_filechooser(self):
        self.explorer = configuration.get_conf("player", "show_explorer", "bool")
        if not (self.explorer):
            self.file_box.hide()
            self.file_chooser__.folder = self.file_chooser__.file_.get_current_folder()
            return
        self.file_box.show()
        self.file_chooser__.file_.set_current_folder(self.file_chooser__.folder)
        self.file_chooser__.file_.grab_focus()

    def repeat_dialog(self, data=None):
        dialog_ = Gtk.Dialog()
        dialog_.run()

    def main(self):
        Gtk.main()
