#!/usr/bin/env python

import pprint
import os

from mothmusicplayer3 import mediaInfo2


class playlist_parser:
    def file_path(self):
        return os.path.split(os.path.abspath(__file__))[0] + '/playlist.m3u'


    # return a list of music files in the
    def __init__(self):
        self.media_ = mediaInfo2.mediaTag()
        self.internal_playlist = self.file_path()
        self.playlist = self.internal_playlist
        self.path_s = ""
        self.external_playlist_flag = False

    def get_items_from_playlist(self, path, path_suffix="none"):
        MUSIC_FILES = None

        if path_suffix != "none":
            if self.external_playlist_flag:
                path_suffix = os.path.dirname(self.playlist) + "/"
            else:
                path_suffix = ""
        else:
            path_suffix = ""

        with open(path, "r") as filee:
            #ignore comments and emptty lines
            if filee.readline() != "##EXTM3U\n" and filee.readline() != "\n":
                filee.seek(0, 0)
                MUSIC_FILES = [path_suffix + LINE.strip() for LINE in filee.readlines() if
                               not LINE.startswith('#') and not LINE.startswith("\n")]
                filee.close()
            else:
                print("EXTM3U")
                #implement extm3u parser here
                filee.close()

        #print MUSIC_FILES
        return MUSIC_FILES

    def put_item_into_playlist(self, path, item):
        with open(path, "r+") as filee:
            #move the cursor to the end of the file
            filee.seek(0, 2)
            if filee.tell() == 0:
                prefix = ""
            else:
                prefix = "\n"
            #add the item
            filee.write(prefix + str(item))
            filee.close()

    def empty_playlist(self, path):
        with open(path, "r+") as filee:
            #delete the content of the file
            filee.truncate()
            filee.close()

    def delete_item_by_number(self, path, number):
        items = self.get_items_from_playlist(path)
        del items[number - 1]
        #print items


        with open(path, "w") as filee:
            counter = 0
            for item in items:
                counter = counter + 1
                if counter == len(items):
                    filee.write(item)
                else:
                    filee.write(item + "\n")

            filee.close()

    def load_external_playlist(self, path):
        self.playlist = path
        self.external_playlist_flag = True

    def load_internal_playlist(self):
        self.playlist = self.internal_playlist
        self.external_playlist_flag = False

    def load_external_playlist_into_internal(self, path, mode):
        #mode: "w" overWrite
        #      "a" append - add to the internal playlist(library)
        items = self.get_items_from_playlist(path, path)

        #needs a better implementation
        if mode == "w":
            self.empty_playlist(path)
        for item in items:
            self.put_item_into_playlist("playlist.m3u", item)

    def search_playlist(self, query):
        items = self.get_items_from_playlist(self.playlist)
        list_ = list()
        for item in items:
            if query.lower() in self.media_.track_get_title(item).lower() or \
                            query.lower() in self.media_.track_get_artist(item).lower() or \
                            query.lower() in self.media_.track_get_album(item).lower():
                list_.append((item, items.index(item)))

        return list_
