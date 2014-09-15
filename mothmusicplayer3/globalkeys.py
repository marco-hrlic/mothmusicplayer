#!/usr/bin/env python

import logging

from keybinder.keybinder_gtk import KeybinderGtk

from mothmusicplayer3 import configuration


logging.basicConfig(format=str(configuration.get_conf("logger", "format", "string")), level=logging.DEBUG)


class keybind:
    def __init__(self, player, gui):
        self.player = player
        self.gui = gui
        self.get_keybindings()
        self.binder = KeybinderGtk()

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
        # call_play =lambda *args: self.gui.player_controls__.play_button_pressed()
        call_play = lambda *args: print("hahahhaha")
        call_pause = lambda *args: self.player.pause_track()
        call_next = lambda *args: self.player.start_next_track_from_playlist()
        call_prev = lambda *args: self.player.start_previous_track_from_playlist()
        call_volup = lambda *args: self.player.volume_track_up()
        call_voldown = lambda *args: self.player.volume_track_down()
        try:
            # play
            self.binder.register(self.play_keystr, call_play)
        except:
            logging.debug("binding failed")

        try:
            # pause
            self.binder.register(self.pause_keystr, call_pause)
        except:
            logging.debug("binding failed")

        try:
            # next
            self.binder.register(self.next_keystr, call_next)
        except:
            logging.debug("binding failed")

        try:
            # prev
            self.binder.register(self.prev_keystr, call_prev)
        except:
            logging.debug("binding failed")

        try:
            # vol-up
            self.binder.register(self.volup_upkeystr, call_volup)
        except:
            logging.debug("binding failed")

        try:
            # vol-down
            self.binder.register(self.voldown_keystr, call_voldown)
        except:
            logging.debug("binding failed")
        self.binder.start()
