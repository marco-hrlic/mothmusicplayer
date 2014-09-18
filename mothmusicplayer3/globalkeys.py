#!/usr/bin/env python

import logging
import gi
from keybinder.keybinder_gtk import KeybinderGtk
from mothmusicplayer3 import configuration


logging.basicConfig(format=str(configuration.get_conf("logger", "format", "string")), level=logging.DEBUG)


class keybind:
    def __init__(self, player, gui):
        self.player = player
        self.gui = gui
        self.get_keybindings()

    def get_keybindings(self):
        logging.debug("getting the keybindings from config file")
        self.play_keystr = str(configuration.get_conf("keybindings", "play", "string"))
        self.pause_keystr = str(configuration.get_conf("keybindings", "pause", "string"))
        self.next_keystr = str(configuration.get_conf("keybindings", "next", "string"))
        self.prev_keystr = str(configuration.get_conf("keybindings", "prev", "string"))
        self.volup_upkeystr = str(configuration.get_conf("keybindings", "volup", "string"))
        self.voldown_keystr = str(configuration.get_conf("keybindings", "voldown", "string"))
        self.file_keystr = str(configuration.get_conf("keybindings", "file_show", "string"))

    def bind_keys(self):
        logging.debug("binding the keys to the related functions")
        """self.binder = KeybinderGtk()
        call_play = lambda *args: self.gui.player_controls__.play_button_pressed()
        call_pause = lambda *args: self.player.pause_track()
        call_next = lambda *args: self.player.start_next_track_from_playlist()
        call_prev = lambda *args: self.player.start_previous_track_from_playlist()
        call_volup = lambda *args: self.player.volume_track_up()
        call_voldown = lambda *args: self.player.volume_track_down()

        # play
    
        self.binder.register(self.play_keystr,call_play)

        # pause
        self.binder.register(self.pause_keystr, call_pause)

        # next
        self.binder.register(self.next_keystr, call_next)

        # prev
        self.binder.register(self.prev_keystr, call_prev)

        # vol-up
        self.binder.register(self.volup_upkeystr, call_volup)

        # vol-down
        self.binder.register(self.voldown_keystr, call_voldown)
        self.binder.start()"""
