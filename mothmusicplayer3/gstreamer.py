#!/usr/bin/env python

import os
import threading
import logging
import queue

from gi.repository import Gst
from gi.repository import GObject

from mothmusicplayer3 import configuration
from mothmusicplayer3 import timeConverter


# logging.basicConfig(format=str(configuration.get_conf("logger", "format", "string")), level=logging.DEBUG)
loop = GObject.MainLoop()


class Player(threading.Thread):
    def exit_player(self):

        #stop the track
        self.player.set_state(Gst.State.NULL)
        #self.vol.exit_()
        #stop the gobject loop
        loop.quit()
        exit(0)
        logging.debug("shutting down the player")

    def run(self):
        logging.debug("initalizing the player")
        #initialize the loop for thread
        GObject.threads_init()
        Gst.init(None)
        #start the loop
        loop.run()

    def get_gui(self, gui_):
        self.gui = gui_

    def __init__(self, playlistt, fader):

        threading.Thread.__init__(self)
        self.filepath = ""
        self._filepath = ""
        self.ffilepath = ""
        self.nowplaying = False
        self.gui = None
        self.vol = fader

        Gst.init_check(None)
        self.ISGST010 = Gst.version()[0] == 0

        self.player = Gst.ElementFactory.make("playbin", "player")
        self.equalizer = Gst.ElementFactory.make("equalizer-10bands", "equalizer-10bands")

        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        self.player.set_property("video-sink", fakesink)

        audioconvert = Gst.ElementFactory.make('audioconvert', "audioconvert")
        audiosink = Gst.ElementFactory.make('autoaudiosink', "audiosink")
        sinkbin = Gst.Bin()
        sinkbin.add(self.equalizer)
        sinkbin.add(audioconvert)
        sinkbin.add(audiosink)
        #Gst.element_link_many(self.equalizer, audioconvert, audiosink)

        self.equalizer.link(audioconvert)
        audioconvert.link(audiosink)

        sinkpad = self.equalizer.get_static_pad('sink')
        sinkbin.add_pad(Gst.GhostPad.new('sink', sinkpad))
        self.player.set_property('audio-sink', sinkbin)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

        self.player.connect("about-to-finish", self.about_to_finish)

        self.playlist_instance = playlistt

        self.time_format = Gst.Format(Gst.Format.TIME)
        self.duration = None
        self.new_file = False
        self.is_playing = False
        self.is_paused = False
        self.current_position = ""
        self.current_track_playlist_index = -2
        self.gapless_playback_flag = True
        self.track_queue = queue.Queue()

        self.music_items = self.playlist_instance.get_items_from_playlist(self.playlist_instance.playlist)

    def index_change(self, number):
        if number - 1 < self.current_track_playlist_index:
            self.current_track_playlist_index = self.current_track_playlist_index - 1

    def enque(self, index):
        self.track_queue.put(index)

    def empty_queue(self):
        self.track_queue.queue.clear()

    def about_to_finish(self, player):
        logging.debug("about_to_finish")
        if bool(configuration.get_conf("player", "repeat")):
            self.load_track_from_playlist(self.playlist_instance.playlist, self.current_track_playlist_index)
            return
        if not self.track_queue.empty():
            self.current_track_playlist_index = self.track_queue.get() + 1
        else:
            self.current_track_playlist_index += 1
        self.load_track_from_playlist(self.playlist_instance.playlist, self.current_track_playlist_index)


    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            pass
        elif t == Gst.MessageType.ERROR:
            self.player.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error: %s" % err, debug)
            self.is_playing = False

    def load_track_from_playlist(self, playlist_path, index_):
        logging.debug("loading track from playlist")
        self.music_items = self.playlist_instance.get_items_from_playlist(playlist_path)

        if index_ >= 0:
            if index_ <= len(self.music_items):
                self.item_to_play = self.music_items[index_ - 1]
                self.current_track_playlist_index = index_
            else:
                if bool(configuration.get_conf("player", "repeat_all")):
                    self.item_to_play = self.music_items[0]
                    self.current_track_playlist_index = 1
                else:
                    return False
        else:
            return False

        #pass the track path to load_track_method
        self.load_track(self.item_to_play)
        #notify gui that there is a song change
        self.gui.playlist__.playlist_selection_change(self.current_track_playlist_index - 1)
        #if everything went ok return TRUE
        return True

    def set_track(self):
        self.player.set_property("uri", self.filepath)
        logging.debug("set the player uri to the filepath")

    def load_track(self, input_path):
        logging.debug("load_track")
        if os.path.isfile(input_path):
            self.filepath = "file://" + input_path
            self._filepath = input_path
            self.new_file = True
            #if not self.is_playing:
            self.set_track()
            #print "  <loaded: " + input_path
        else:
            print("  file path error!")

    def start_track(self, data=None):
        logging.debug("starting the track")
        self.player.set_state(Gst.State.PLAYING)
        self.is_playing = True
        self.new_file = False
        self.gui.player_controls__.start_stop_bar_animation()

    def start_next_track_from_playlist(self, data=None):
        logging.debug("load and start next track from playlist if possible")
        if self.is_playing or self.is_paused:
            self.player.set_state(Gst.State.NULL)
            self.is_playing = False
            self.is_paused = False
            timer = self.gui.timer
            if timer is not None:
                GObject.source_remove(timer)

        self.current_track_playlist_index += 1
        #try to load the track from playlist
        if self.load_track_from_playlist(self.playlist_instance.playlist, self.current_track_playlist_index):
            self.player.set_state(Gst.State.PLAYING)
            self.is_playing = True
            timer = GObject.timeout_add(1000, self.gui.player_controls__.seek_bar__.update_time_label)
        else:
            #if loading fails the track didnt change
            self.current_track_playlist_index -= 1

    def start_previous_track_from_playlist(self, data=None):
        logging.debug("loading and starting previous track from playlist if possible")
        if self.is_playing or self.is_paused:
            self.player.set_state(Gst.State.NULL)
            self.is_playing = False
            self.is_paused = False
            timer = self.gui.timer
            if timer is not None:
                GObject.source_remove(timer)

        self.current_track_playlist_index -= 1
        #try to load the track from playlist
        if self.load_track_from_playlist(self.playlist_instance.playlist, self.current_track_playlist_index):
            self.player.set_state(Gst.State.PLAYING)
            self.is_playing = True
            timer = GObject.timeout_add(1000, self.gui.player_controls__.seek_bar__.update_time_label)
        else:
            #if loading fails the track didnt change
            self.current_track_playlist_index += 1

    def stop_track(self, data=None):
        self.player.set_state(Gst.State.NULL)
        self.is_playing = False
        self.is_paused = False

    def pause_track(self, data=None):
        logging.debug("pausing the track")
        if bool(configuration.get_conf("effects", "pause_fade")):
            self.vol.fade_effect_out(self.player, self.volume_show_track(), 0.5, 100)

        self.player.set_state(Gst.State.PAUSED)
        self.is_playing = False
        self.is_paused = True
        self.gui.player_controls__.start_stop_bar_animation()

    def volume_track_up(self, data=None):
        value = self.volume_show_track()
        if not value >= 100:
            value += 10
            self.volume_track(value)

    def volume_track_down(self, data=None):
        value = self.volume_show_track()
        if not value < 10:
            value -= 10
            self.volume_track(value)

    def volume_track_by(self, value_, up_down):
        value = self.volume_show_track()
        if up_down == "down":
            value -= value_
        else:
            value += value_
        if not (value < 0 and value > 100):
            self.volume_track(value)

    def volume_track(self, value):
        if not (value < 0 and value > 100):
            print(value)
            self.player.set_property("volume", value / 100)
            if not self.gui == None:
                self.gui.player_controls__.update_volume_slider()

    def volume_show_track(self):
        volume_value = float(self.player.get_property("volume"))
        return float(volume_value) * 100

    def get_current_position_track(self):
        if self.is_playing or self.is_paused:
            self.current_position = self.player.query_position(self.time_format)[1]
            self.current_position_formated = timeConverter.convert_time(self.current_position)
            return self.current_position_formated
        else:
            return None

    def get_current_position_track_unformatted(self):
        if self.is_playing or self.is_paused:
            self.current_position = self.player.query_position(self.time_format)[1]
            return self.current_position
        else:
            return None

    def set_position_track(self, value):
        #get the duration
        duration = self.player.query_duration(self.time_format)[1]
        #explicit type casting
        time = value
        self.player.seek_simple(self.time_format, Gst.SeekFlags.FLUSH, time)

    def get_duration(self):
        return self.player.query_duration(self.time_format)[1]


    def eq_get(self):
        eq_list = list()
        for x in range(1, 11):
            value = self.equalizer.get_property("band" + str(int(x) - 1))
            eq_list.append(int(value))
        return eq_list

    def eq_set(self, band, value):
        if int(value) in range(-24, 12):
            self.equalizer.set_property("band" + str(int(band) - 1), value)
        

        
