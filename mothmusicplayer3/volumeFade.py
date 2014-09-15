#!usr/bin/python2

import threading
# import pygst
#pyGst.require("0.10")
import time


class volume_fader(threading.Thread):
    def run(self):
        pass

    def __init__(self):
        threading.Thread.__init__(self)

    #fade duration in s
    def fade_effect_out(self, player, current_volume, fade_duration, fade_steps):
        self.sleep_interval = fade_duration / fade_steps
        self.value = current_volume / 100
        self.decrease_value = self.value / float(fade_steps)

        for x in range(1, fade_steps):
            self.value -= self.decrease_value
            player.set_property("volume", self.value)
            time.sleep(self.sleep_interval)
        #player.set_state(Gst.State.PAUSED)
        player.set_property("volume", current_volume / 100)

    def exit_(self):
        print("vol")
        exit(0)
