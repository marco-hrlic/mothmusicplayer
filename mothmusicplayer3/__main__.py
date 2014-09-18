#!/usr/bin/env python

from mothmusicplayer3 import gstreamer
from mothmusicplayer3 import volumeFade
from mothmusicplayer3 import playlist
from mothmusicplayer3 import gui_builder
from mothmusicplayer3 import globalkeys
# initalize classes

class mothmusicplayer:
    def __init__(self):
        #volume = volumeFade.volume_fader()
        volume = None
        playlist_ = playlist.playlist_parser()
        gst = gstreamer.Player(playlist_, volume)
        #cmd = cmdDebug.cmdDbg(gst, playlist)
        gui = gui_builder.main_window(gst, playlist_)


        #set up the keybinder
        keys = globalkeys.keybind(gst, gui)
        keys.bind_keys()
        gui.player_controls__.settings.get_keybinder(keys)


        #send the gui to gst
        gst.get_gui(gui)

        #start threads
        #volume.start()
        #cmd.start()
        gst.start()
        gui.main()


def main_application():
    moth = mothmusicplayer()


if __name__ == "__main__":
    main_application()
