#!/usr/bin/env python2


def convert_time(time=None):
    # convert_ns function from:
    # http://pygstdocs.berlios.de/pygst-tutorial/seeking.html
    # LGPL Version 3 - Copyright: Jens Persson
    if time == None:
        return None

    hours = 0
    minutes = 0
    seconds = 0
    time_string = ""

    time = time / 1000000000  # Gst.NSECOND

    if time >= 3600:
        hours = time / 3600
        time = time - (hours * 3600)
    if time >= 60:
        minutes = int(time / 60)
        time = time - (minutes * 60)
        # remaining time is seconds
    seconds = int(time)

    time_string = time_string + str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    #return time in Hours:Minutes:Seconds format
    return time_string


def convert_time_back(time):
    result = 0
    time_split = time.split(':')
    result = result + int(time_split.pop(0)) * 3600 * 1000000000
    result = result + int(time_split.pop(0)) * 60 * 1000000000
    result = result + int(time_split.pop(0)) * 1000000000
    return result
