#! usr/bin/env python

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, GdkPixbuf
from mothmusicplayer3 import configuration
from mothmusicplayer3 import seekbar_gui
from mothmusicplayer3 import settings_gui
import logging

logging.basicConfig(format=str(configuration.get_conf("logger", "format", "string")), level=logging.DEBUG)


class player_controls_:
    def __init__(self, parent_class):
        self.parent = parent_class
        self.player = self.parent.player
        self.timer = self.parent.timer
        self.settings = settings_gui.preferences_gui(self)

    def volume_value_changed(self, volumebutton, value):
        self.player.volume_track(value * 100)

    def update_volume_slider(self):
        logging.debug("updating the volume slider")
        self.volume_button.set_value(self.player.volume_show_track() / 100)

    def player_controls(self):

        # make a box to pack the buttons in
        box = Gtk.HBox(False, 5)
        box.set_border_width(5)

        spacer1 = Gtk.VSeparator()
        spacer2 = Gtk.VSeparator()



        #declare images
        image_play = Gtk.Image()
        image_pause = Gtk.Image()
        image_prev = Gtk.Image()
        image_next = Gtk.Image()
        image_repeat = Gtk.Image()
        image_pref = Gtk.Image()
        self.image_bars = Gtk.Image()

        #set images
        if(bool(configuration.get_conf("apperance", "use_system_gtk_theme"))):
            image_play.set_from_stock(Gtk.STOCK_MEDIA_PLAY, Gtk.IconSize.BUTTON)
            image_pause.set_from_stock(Gtk.STOCK_MEDIA_PAUSE, Gtk.IconSize.BUTTON)
            image_prev.set_from_stock(Gtk.STOCK_MEDIA_PREVIOUS, Gtk.IconSize.BUTTON)
            image_next.set_from_stock(Gtk.STOCK_MEDIA_NEXT, Gtk.IconSize.BUTTON)
            image_repeat.set_from_stock(Gtk.STOCK_REFRESH, Gtk.IconSize.BUTTON)
            image_pref.set_from_stock(Gtk.STOCK_PREFERENCES, Gtk.IconSize.BUTTON)
        else:
            image_play.set_from_file("mmp_icons/media-playback-start.svg")
            image_pause.set_from_file("mmp_icons/media-playback-pause.svg")
            image_prev.set_from_file("mmp_icons/media-skip-backward.svg")
            image_next.set_from_file("mmp_icons/media-skip-forward.svg")
            image_repeat.set_from_file("mmp_icons/view-refresh.svg")
            image_pref.set_from_stock(Gtk.STOCK_PREFERENCES, Gtk.IconSize.BUTTON)

        self.bar_animation = GdkPixbuf.PixbufAnimation.new_from_file("mmp_icons/bar1.gif") 
        self.image_bars.set_from_pixbuf(self.bar_animation.get_static_image())

        #declare buttons
        self.play_button = Gtk.Button()
        self.play_button.set_image(image_play)
        self.play_button.props.relief = Gtk.ReliefStyle.NONE
        self.play_button.set_focus_on_click(False)

        self.pause_button = Gtk.Button()
        self.pause_button.set_image(image_pause)
        self.pause_button.props.relief = Gtk.ReliefStyle.NONE
        self.pause_button.set_focus_on_click(False)

        self.prev_button = Gtk.Button()
        self.prev_button.set_image(image_prev)
        self.prev_button.props.relief = Gtk.ReliefStyle.NONE
        self.prev_button.set_focus_on_click(False)
        self.next_button = Gtk.Button()
        self.next_button.set_image(image_next)
        self.next_button.props.relief = Gtk.ReliefStyle.NONE
        self.next_button.set_focus_on_click(False)

        self.repeat_button = Gtk.ToggleButton()
        self.repeat_button.set_image(image_repeat)
        self.repeat_button.props.relief = Gtk.ReliefStyle.NONE
        self.repeat_button.set_focus_on_click(False)
        state = configuration.get_conf("player", "repeat")
        if bool(state):
            self.repeat_button.set_active(True)

        self.pref_button = Gtk.Button()
        self.pref_button.set_image(image_pref)
        self.pref_button.props.relief = Gtk.ReliefStyle.NONE
        self.pref_button.set_focus_on_click(False)

        #initalize volume 
        self.volume_button = Gtk.VolumeButton()
        self.volume_button.set_value(float(configuration.get_conf("player", "volume", "int")) / 100)

        self.volume_button.connect("value-changed", self.volume_value_changed)
        self.player.volume_track(self.volume_button.get_value() * 100)

        #self.seek_bar_ = self.seek_bar()
        self.seek_bar__ = seekbar_gui.seek_bar_(self.player)
        self.seek_bar_ = self.seek_bar__.seek_bar()

        #pack the buttons
        box.pack_start(self.play_button, False, True, 0)
        box.pack_start(self.pause_button, False, True, 0)
        box.pack_start(self.prev_button, False, True, 0)
        box.pack_start(self.next_button, False, True, 0)
        box.pack_start(spacer1, False, True, 10)
        box.pack_start(self.repeat_button, False, True, 0)
        box.pack_start(spacer2, False, True, 10)
        box.pack_start(self.image_bars, False, True, 0)
        box.pack_start(self.seek_bar_, True, True, 0)
        box.pack_start(self.volume_button, False, True, 0)
        box.pack_start(self.pref_button, False, False, 10)

        #show everything
        spacer1.show()
        spacer2.show()
        self.play_button.show()
        self.pause_button.show()
        self.prev_button.show()
        self.next_button.show()
        self.repeat_button.show()
        self.pref_button.show()
        self.volume_button.show()
        self.image_bars.show()
        box.show()
        return box

    def start_stop_bar_animation(self):
        if(self.player.is_playing):
            self.image_bars.set_from_animation(self.bar_animation)
        else:
            self.image_bars.set_from_pixbuf(self.bar_animation.get_static_image())

    def connect_handlers(self):
        self.play_button.connect("pressed", self.play_button_pressed)
        self.pause_button.connect("pressed", self.player.pause_track)
        self.prev_button.connect("pressed", self.player.start_previous_track_from_playlist)
        self.next_button.connect("pressed", self.player.start_next_track_from_playlist)
        self.pref_button.connect("pressed", self.open_settings)
        self.repeat_button.connect("pressed", self.repeat_button_callback)

    def open_settings(self, data=None):
        if not self.settings.is_shown:
            self.settings.show_settings_window()

    def repeat_button_callback(self, button):
        state = button.get_active()
        configuration.set_conf("player", "repeat", str(not bool(state)))

    def play_button_pressed(self, data=None):
        logging.debug("play action has occured(button or invoked from code)")
        if not self.player.is_playing and not self.player.is_paused:
            selection = self.parent.playlist__.treeView.get_selection()
            rows = selection.get_selected_rows()[1]
            treeiter = self.parent.playlist__.store.get_iter(rows[0])
            path = self.parent.playlist__.store.get_path(treeiter)
            self.parent.playlist__.row_activated(self.parent.playlist__.treeView, path, None,
                                                 self.parent.playlist__.store)

        if self.player.is_paused:
            self.player.start_track()
            self.timer = GObject.timeout_add(1000, self.seek_bar__.update_time_label)
        if self.player.is_playing:
            selection = self.parent.playlist__.treeView.get_selection()
            rows = selection.get_selected_rows()[1]
            treeiter = self.parent.playlist__.store.get_iter(rows[0])
            path = self.parent.playlist__.store.get_path(treeiter)
            value = path[0]
            if not self.player.current_track_playlist_index == (value + 1):
                self.parent.playlist__.row_activated(self.parent.playlist__.treeView, path, None, self.parent.playlist__.store)

