#!/usr/bin/env python

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from mothmusicplayer3 import configuration


class console:
    def __init__(self, parent):
        self.parent = parent
        self.is_visible = False
        self.box = None
        self.show_flag = bool(configuration.get_conf("player", "show_console", "bool"))
        self.comm_flag = False

    def show_hide(self, flag=False):
        self.show_flag = bool(configuration.get_conf("player", "show_console", "bool"))
        if self.show_flag and flag:
            self.box.show()
            self.is_visible = True
        else:
            self.textbox.set_text("")
            self.box.hide()
            self.is_visible = False

    def get_tokens(self, text):

        tokens = text.split(" ")
        return tokens

    def evaluate(self, text):
        tokens = self.get_tokens(text)
        if tokens[0] == ":set":
            if tokens[1] == "repeat":
                state = tokens[2] in ["true", "True", "TRUE", "1", "t"]
                configuration.set_conf("player", "repeat", bool(state))
                return False
            if tokens[1] == "repeat_all":
                state = tokens[2] in ["true", "True", "TRUE", "1", "t"]
                configuration.set_conf("player", "repeat_all", bool(state))
                return False
            if tokens[1] == "show_places":
                if configuration.get_conf("player", "show_explorer", "bool"):
                    state = tokens[2] in ["true", "True", "TRUE", "1", "t"]
                    configuration.set_conf("file_chooser", "show_places", state)
                    self.parent.file_chooser__.file_chooser_places_show_hide()
                return False
            if tokens[1] == "show_explorer":
                state = tokens[2] in ["true", "True", "TRUE", "1", "t"]
                configuration.set_conf("player", "show_explorer", state)
                self.parent.show_hide_filechooser()
                return False
            if tokens[1] == "vol":
                self.parent.player.volume_track(float(tokens[2]))
                return False
        elif tokens[0] == ":r":
            configuration.set_conf("player", "repeat", not configuration.get_conf("player", "repeat", "bool"))
            return False
        elif tokens[0] == ":ra":
            configuration.set_conf("player", "repeat_all", not configuration.get_conf("player", "repeat_all", "bool"))
            return False
        elif tokens[0] == ":e":
            state = configuration.get_conf("player", "show_explorer", "bool")
            configuration.set_conf("player", "show_explorer", not state)
            self.parent.show_hide_filechooser()
            return False
        elif tokens[0] == ":i":
            state = configuration.get_conf("player", "show_infobar", "bool")
            configuration.set_conf("player", "show_infobar", not state)
            self.parent.infobar.show_hide()
            return False
        elif tokens[0] == ":s" or tokens[0] == ":settings":
            self.parent.player_controls__.settings.show_settings_window()
        elif tokens[0] == ":vol" or tokens[0] == ":v":
            if len(tokens) == 3:
                if tokens[1] == "up" or tokens[1] == "u":
                    self.parent.player.volume_track_by(int(tokens[2]), "up")
                if tokens[2] == "down" or tokens[1] == "d":
                    self.parent.player.volume_track_by(int(tokens[2]), "down")
            elif len(tokens) == 2:
                self.parent.player.volume_track(float(tokens[1]))
            return False
        elif tokens[0] == ":pause" or tokens[0] == ":pa":
            self.parent.player.pause_track()
            return False
        elif tokens[0] == ":play" or tokens[0] == ":pl" or tokens[0] == ":p":
            if len(tokens) == 1:
                self.parent.player_controls__.play_button_pressed()
            else:
                if int(tokens[1]) < len(self.parent.playlist__.store):
                    self.parent.playlist__.playlist_selection_change(int(tokens[1]))
                    self.parent.player_controls__.play_button_pressed()
            return False
        elif len(tokens) == 1 and (tokens[0][1:].isdigit()):
            if int(tokens[0][1:]) < len(self.parent.playlist__.store):
                self.parent.playlist__.playlist_selection_change(int(tokens[0][1:]))
                self.parent.player_controls__.play_button_pressed()
            return False
        elif tokens[0] == ":next" or tokens[0] == ":ne":
            self.parent.player.start_next_track_from_playlist()
            return False
        elif tokens[0] == ":prev" or tokens[0] == ":pr":
            self.parent.player.start_previous_track_from_playlist()
            return False
        elif tokens[0] == ":q":
            self.parent.destroy(None)
            return False
        elif tokens[0] == ":que":
            for x in range(1, len(tokens)):
                self.parent.player.enque(int(tokens[x]))
            self.parent.playlist__.update_queue()
            return False
        elif tokens[0] == ":qe":
            self.parent.player.empty_queue()
            self.parent.playlist__.update_queue()
            return False
        elif tokens[0] == ":d":
            if len(tokens) == 1:
                self.parent.playlist__.remove_selected(None, self.parent.playlist__.treeView)
            return False
        elif tokens[0] == ":da":
            self.parent.playlist__.select_all(None, self.parent.playlist__.treeView)
            self.parent.playlist__.remove_selected(None, self.parent.playlist__.treeView)
            return False
        return True

    def output(self, output_line):
        self.textbox.set_text("")
        self.textbox.set_text(output_line)
        self.textbox.set_position(len(output_line))
        self.comm_flag = True

    def textbox_callback(self, widget, entry):
        if bool(configuration.get_conf("player", "show_console", "bool")):
            if self.comm_flag:
                self.show_hide()
                self.comm_flag = False
                return
            text = widget.get_text()
            result = self.evaluate(text)
            if (result):
                self.output("Unknown command")
            else:
                self.show_hide()

    def focus_out(self, widget, event):
        self.comm_flag = False
        self.show_hide()

    def key_press(self, widget, event):
        keyname = Gdk.keyval_name(event.keyval)
        if keyname == "Escape":
            self.show_hide()
            self.comm_flag = False

    def console_gui(self):
        self.box = Gtk.HBox(True, 10)
        self.textbox = Gtk.Entry()
        self.box.pack_start(self.textbox, True, True, 0)

        self.textbox.connect("activate", self.textbox_callback, self.textbox)
        self.textbox.connect("focus_out_event", self.focus_out)
        self.textbox.connect("key_press_event", self.key_press)
        self.textbox.show()
        self.show_hide()
        return self.box
