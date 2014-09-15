#! usr/bin/env python

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gst
from mothmusicplayer3 import timeConverter


class seek_bar_:
    def __init__(self, player):
        self.is_seeking = False
        self.percent = 0
        self.duration = None
        self.player = player

    def update_time_label(self, flag=False):

        if flag:
            self.time_label.set_text("0:00/0:00")
            return False
        self.duration = None
        self.current_position = None
        self.length = None
        self.percent = None
        self.ad = None

        if (not self.player.is_paused) and self.player.is_playing == False:
            # print "return false"
            return False
        if self.duration == None:
            try:
                self.length = self.player.get_duration()
                self.duration = timeConverter.convert_time(self.length)
            except:
                self.duration = None

        if self.duration != None:
            self.current_position = self.player.get_current_position_track()


            # Update the seek bar
            # Gtk.Adjustment(value=0, lower=0, upper=0, step_incr=0, page_incr=0, page_size=0)
            if not self.is_seeking:
                self.time_label.set_text(self.current_position[4:] + "/" + self.duration[4:])
                self.percent = (
                               float(self.player.get_current_position_track_unformatted()) / float(self.length)) * 100.0
                self.ad = Gtk.Adjustment.new(self.percent, 0.00, 100.0, 0.5, 0.5, 1.0)
                # if not self.is_seeking:
                self.hscale.set_adjustment(self.ad)

        return True

    def seeking_value(self, range, scroll, value):
        if self.player.is_playing or self.player.is_paused:
            duration = self.player.player.query_duration(Gst.Format(Gst.Format.TIME))[1]
            time = timeConverter.convert_time(int((value / 100) * duration))
            self.length = self.player.get_duration()
            self.duration = timeConverter.convert_time(self.length)

            # quick hack not a complete solution! needs fixing!
            if int(time[6:]) > int(self.duration[6:]) or int(time[4:5]) > int(self.duration[4:5]):
                if not self.player.is_paused:
                    return
            self.time_label.set_text(time[4:] + "/" + self.duration[4:])

    def seeker_event(self, widget, event):
        if self.player.is_playing or self.player.is_paused:
            value = widget.get_value()
            duration = self.player.player.query_duration(Gst.Format(Gst.Format.TIME))[1]
            time = value * (duration / 100)
            self.player.player.seek_simple(Gst.Format(Gst.Format.TIME), Gst.SeekFlags.FLUSH, time)
            if self.is_seeking:
                self.hscale.disconnect(self.handler_id)
            self.is_seeking = False


    def set_seeking(self, widget, data=None):
        # TRYING THINGS MIGHT BREAK STUFF!!!!!!
        print("set_seeking------------------------")
        if self.player.is_playing or self.player.is_paused:
            self.is_seeking = True
            adjustment = Gtk.Adjustment(self.percent, 0.00, 100.0, 0.5, 0.5, 1.0)
            print("handler")
            self.hscale.set_adjustment(adjustment)
            self.handler_id = self.hscale.connect("change-value", self.seeking_value)


    def seek_bar(self):
        self.time_text = "0:00/0:00"
        box = Gtk.HBox(False, 5)
        spacer = Gtk.VSeparator()

        self.time_label = Gtk.Label(label=self.time_text)

        # self.update_time_label()
        self.hscale = Gtk.HScale()
        self.hscale.set_draw_value(False)
        self.hscale.set_value_pos(Gtk.PositionType.LEFT)
        #self.hscale.set_update_policy(Gtk.UPDATE_DISCONTINUOUS)
        self.hscale.connect("button-release-event", self.seeker_event)
        self.hscale.connect("button-press-event", self.set_seeking)
        self.hscale.set_can_focus(False)

        box.pack_start(self.time_label, False, False, 5)
        box.pack_start(spacer, False, False, 10)
        box.pack_start(self.hscale, True, True, 5)

        self.time_label.show()
        self.hscale.show()
        box.show()

        return box
