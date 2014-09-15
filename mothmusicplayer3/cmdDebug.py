#!/usr/bin/env python2

import sys
import os
import threading

from mothmusicplayer3 import gstreamer
from mothmusicplayer3 import mediaInfo2
from mothmusicplayer3 import timeConverter
from mothmusicplayer3 import configuration
from mothmusicplayer3 import playlist
from mothmusicplayer3 import colorPrint


load_path = None


class cmdDbg(threading.Thread):
    def __init__(self, player, playlisttt):
        threading.Thread.__init__(self)

        os.system("clear")

        self.cmdInput = None
        self._player = player
        self.pp = playlisttt
        self.color = colorPrint.bcolors()
        self.mediaInfo = mediaInfo2.mediaTag()

        print(self.color.HEADER + "<---- mOTHmUSICpLAYER ---->" + self.color.ENDC + "\n")

        # load on startup
        if bool(configuration.get_conf("player", "remember_last_track")):
            self.pp.external_playlist_flag = True
            item = self.pp.get_items_from_playlist("last_track_and_playlist", "none")
            #print item
            self.pp.playlist = item[2]
            if len(item) == 3:
                load_index = 1
            else:
                load_index = int(item[3].strip())

            self._player.load_track_from_playlist(self.pp.playlist, load_index)

        elif bool(configuration.get_conf("player", "load_from_playlist_on_startup")):
            self._player.load_track_from_playlist(self.pp.playlist, int(0))

        #load the eq
        for x in range(1, 11):
            value = configuration.get_conf("eq", "band" + str(int(x) - 1), "int")
            self._player.eq_set(int(x), int(value))


    def run(self):
        self.cmd_input()

    def cmd_input(self):

        while 1:
            self.cmdInput = input(self.color.OKBLUE + ":." + self.color.ENDC)

            if self.cmdInput == "load":
                load_path = input("  <path:")
                self._player.load_track(load_path)


            elif self.cmdInput == "load-from-playlist":
                # Display the playlist
                items = self.pp.get_items_from_playlist(self.pp.playlist, "")
                x = 1
                print(self.color.OKGREEN + "\n  <Playlist:\n" + self.color.ENDC)
                for item in items:
                    print("    <" + str(x) + ". " + self.color.OKBLUE + self.mediaInfo.track_get_title(item) + \
                          self.color.ENDC + " - " + \
                          self.mediaInfo.track_get_artist(item) + "\n      path: " + item[0:30] + "...")
                    x = x + 1
                print("\n")
                num = input("  <index of the track to load: ")

                if num > 0:
                    self._player.load_track_from_playlist(self.pp.playlist, int(num))
                else:
                    print(self.color.FAIL + "  <ERROR: index doesn't exist!" + self.color.ENDC)

            elif self.cmdInput == "load-into-playlist":
                path = input("  <path: ")
                self.pp.put_item_into_playlist(self.pp.playlist, path)

            elif self.cmdInput == "copy-into-internal-playlist":
                if self.pp.playlist == self.pp.internal_playlist:
                    print(self.color.ERROR + "  <do you really want to duplicate?!" + self.color.ENDC)
                else:
                    self.pp.load_external_playlist_into_internal(self.pp.playlist, "a")
                    self._player.load_track_from_playlist(self.pp.playlist, 1)

            elif self.cmdInput == "load-playlist":
                path = input("  <path:")
                self.pp.load_external_playlist(path)

            elif self.cmdInput == "load-internal-playlist":
                self.pp.load_internal_playlist()


            elif self.cmdInput == "playlist-search":
                input_ = input("  <query:")
                result_items = self.pp.search_playlist(input_)
                if len(result_items) == 0:
                    print("  <no match")
                else:
                    x = 1
                    print(self.color.OKGREEN + "\n  <Search Reults:\n" + self.color.ENDC)
                    for item in result_items:
                        print("    <" + str(x) + ". " + self.color.OKBLUE + self.mediaInfo.track_get_title(item[0]) + \
                              self.color.ENDC + " - " + \
                              self.mediaInfo.track_get_artist(item[0]) + "\n      path: " + item[0][0:30] + "...")
                        x = x + 1
                    print("\n")
                    num = input("  <do you want to load a track? (index):")
                    if num != "":
                        if int(num) > 0:
                            self._player.load_track_from_playlist(self.pp.playlist,
                                                                  int(result_items[int(num) - 1][1]) + 1)
                        else:
                            print(self.color.FAIL + "  <ERROR: index doesn't exist!" + self.color.ENDC)





            elif self.cmdInput == "play":
                self._player.start_track()

            elif self.cmdInput == "play-next":
                self._player.start_next_track_from_playlist()

            elif self.cmdInput == "play-prev":
                self._player.start_previous_track_from_playlist()

            elif self.cmdInput == "stop":
                self._player.stop_track()

            elif self.cmdInput == "pause":
                self._player.pause_track()

            elif self.cmdInput == "volume-set":
                print(self.color.OKGREEN + "\n    <current: " + str(int(self._player.volume_show_track())) \
                      + self.color.ENDC)
                inp = input("  <set:")
                if inp != "":
                    self._player.volume_track(float(inp))
                print("\n")

            elif self.cmdInput == "info":
                print(self.color.OKGREEN + "\n  <Track Info:\n" + self.color.ENDC)
                print("\n    <     title: " + self.color.OKBLUE + self.mediaInfo.track_get_title(self._player._filepath) \
                      + self.color.ENDC)
                print("    <    artist: " + self.color.OKBLUE + self.mediaInfo.track_get_artist(self._player._filepath) \
                      + self.color.ENDC)
                print("    <     album: " + self.color.OKBLUE + self.mediaInfo.track_get_album(self._player._filepath) \
                      + self.color.ENDC)
                print("    <      year: " + self.color.OKBLUE + self.mediaInfo.track_get_year(self._player._filepath) \
                      + self.color.ENDC)
                print("    <     track: " + self.color.OKBLUE + self.mediaInfo.track_get_track(self._player._filepath) \
                      + self.color.ENDC)
                print("    <     genre: " + self.color.OKBLUE + self.mediaInfo.track_get_genre(self._player._filepath) \
                      + self.color.ENDC)
                print("    <  duration: " + self.color.OKBLUE + \
                      timeConverter.convert_time(
                          self.mediaInfo.track_get_duration(self._player._filepath) * 1000000000) + self.color.ENDC)
                print("    <   bitrate: " + self.color.OKBLUE + self.mediaInfo.track_get_bitrate(self._player._filepath) \
                      + "\n" + self.color.ENDC)

            elif self.cmdInput == "position-get":
                print(self.color.OKGREEN + "\n  <current position: " + self.color.ENDC + \
                      str(self._player.get_current_position_track()) + "\n")

            elif self.cmdInput == "position-set":
                print("\n  <input format: hh:mm:ss")
                inp = input("  <set:")
                if inp != "":
                    self._player.set_position_track(timeConverter.convert_time_back(inp))
                print("\n")

            elif self.cmdInput == "config":
                input_ = input("   <")
                if input_ == "repeat":
                    print(
                        "    <" + self.color.OKBLUE + str(configuration.get_conf("player", "repeat")) + self.color.ENDC)
                    input_ = input("    <")
                    if input_ != "":
                        configuration.set_conf("player", "repeat", input_)

                elif input_ == "fade":
                    print("   <" + self.color.OKBLUE + str(
                        configuration.get_conf("effects", "pause_fade")) + self.color.ENDC)
                    input_ = input("   <")
                    if input_ != "":
                        configuration.set_conf("effects", "pause_fade", input_)

                elif input_ == "remember on exit":
                    print("   <" + self.color.OKBLUE + str(
                        configuration.get_conf("player", "remember_last_track")) + self.color.ENDC)
                    input_ = input("   <")
                    if input_ != "":
                        configuration.set_conf("player", "remember_last_track", input_)

                elif input_ == "load on startup":
                    print("   <" + self.color.OKBLUE + str(
                        configuration.get_conf("player", "load_from_playlist_on_startup")) \
                          + self.color.ENDC)
                    input_ = input("   <")
                    if input_ != "":
                        configuration.set_conf("player", "load_from_playlist_on_startup", input_)


            elif self.cmdInput == "path-get":
                print("  <path: " + self._player.filepath)

            elif self.cmdInput == "playlist-erase-all":
                self.pp.empty_playlist(self.pp.playlist)

            elif self.cmdInput == "playlist-erase":
                items = self.pp.get_items_from_playlist(self.pp.playlist, "")
                x = 1
                for item in items:
                    print("      <" + str(x) + ". " + self.color.OKBLUE + self.mediaInfo.track_get_title(item) + \
                          self.color.ENDC + " - " + \
                          self.mediaInfo.track_get_artist(item) + "\n      path: " + item[0:30] + "...")
                    x = x + 1

                num = input("  <erase item with index: ")
                if num.isdigit():
                    if num > 0:
                        if int(num) > int(len(items)):
                            print(self.color.FAIL + "  <ERROR: index is out of bound" + self.color.ENDC)
                        else:
                            self.pp.delete_item_by_number(self.pp.playlist, int(num))
                    else:
                        print(self.color.FAIL + "  <ERORR: index can't be < 0" + self.color.ENDC)
                else:
                    print(self.color.FAIL + "  <ERROR: invalid input!" + self.color.ENDC)

            elif self.cmdInput == "playlist-get":
                items = self.pp.get_items_from_playlist(self.pp.playlist, "")
                x = 1
                print(self.color.OKGREEN + "\n  <Playlist:\n" + self.color.ENDC)
                for item in items:
                    print("    <" + str(x) + ". " + self.color.OKBLUE + self.mediaInfo.track_get_title(item) + \
                          self.color.ENDC + " - " + \
                          self.mediaInfo.track_get_artist(item) + "\n      path: " + item[0:25] + "...")
                    x = x + 1
                print("\n")



            elif self.cmdInput == "eq-get":
                eq_values = self._player.eq_get()
                for x in range(1, 11):
                    print("  <" + str(x) + ".  band" + str(x - 1) + ": " + str(eq_values[x - 1]))

            elif self.cmdInput == "eq-set":
                print(self._player.eq_get())
                input_band = input("  <band(1-10):")
                input_value = input("  <value(-24 - 12):")
                self._player.eq_set(input_band, int(input_value))
                configuration.set_conf("eq", "band" + str(int(input_band) - 1), str(int(input_value)))

            elif self.cmdInput == "clear":
                os.system("clear")

            elif self.cmdInput == "exit":
                if bool(configuration.get_conf("player", "remember_last_track")):
                    self.pp.empty_playlist("last_track_and_playlist")
                    self.pp.put_item_into_playlist("last_track_and_playlist", self._player._filepath)
                    self.pp.put_item_into_playlist("last_track_and_playlist", self.pp.playlist)
                    self.pp.put_item_into_playlist("last_track_and_playlist", self._player.current_track_playlist_index)

                self.exit_cmd()

            elif not self.cmdInput == "exit":
                print(self.color.FAIL + "  <ERROR: unknown command" + self.color.ENDC)

    def exit_cmd(self):
        # print "exit_cmd"
        self._player.exit_player()
        exit(0)
