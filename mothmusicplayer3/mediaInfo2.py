#!/usr/bin/env python

import os

from mutagenx.flac import FLAC
from mutagenx.mp3 import EasyMP3 as MP3


class mediaTag:
    def reverse(self, s):
        txt = ''
        for i in range(len(s) - 1, -1, -1):
            txt += s[i]
        return txt

    def __init__(self):
        self.file_type = ""
        self.audio = None

    def get_file_type(self, path):
        string = os.path.basename(path)
        # parts = string.split(".")
        file_t = ""
        for c in self.reverse(string):
            if c == '.':
                break
            file_t = file_t + c
        file_t = self.reverse(file_t)
        self.file_type = file_t.upper()
        #self.file_type = parts[1].upper()
        #return parts[1]
        return file_t

    def track_get_title(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)
            data = self.audio["title"]
            return data[0]
        except:
            # return " - "
            title = os.path.basename(path).split("/")[-1]
            return title


    def track_get_artist(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)
            data = self.audio["artist"]
            # print data[0]
            return data[0]
        except:
            return " - "

    def track_get_album(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)
            data = self.audio["album"]
            # print data[0]
            return data[0]
        except:
            return " - "

    def track_get_duration(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)
            # data = audio["length"]
            #print data[0]
            #return data[0]
            return int(audio.info.length)
        except:
            return " - "

    def track_get_bitrate(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)

            return str(self.audio.info.bitrate / 1000)

        except:
            return " - "

    def track_get_genre(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)
            data = self.audio["genre"]
            # print data[0]
            return data[0]
        except:
            return " - "

    def track_get_year(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)
            data = self.audio["date"]
            # print data[0]
            return data[0]
        except:
            return " - "

    def track_get_track(self, path):
        try:
            self.get_file_type(path)
            string = "self.audio = " + self.file_type + "(\"" + path + "\")"
            exec(string)
            data = self.audio["tracknumber"]
            # print data[0]
            return data[0]
        except:
            return " - "
