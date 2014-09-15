##MothMusicPlayer

MMP is a music player for linux written in Python3, GTK3 and Gstreamer,
altough there is a version written in Python2 and pygtk (GTK2).
The project is in a early development stage, there are still some bugs,
the code is messy and
needs major refactoring.

The idea behind this project was to create a simple and lightweight music
player for linux operating systems. The GUI lacks functionality (buttons etc.),
however almost any control can be accessed with vim-like commands:
- :p play
- :pa pause
- :ne next
- :pr prevous
- *...you can have a peak into console.py to see the full list of actions*

To run you will need Python3, GTK3 and Gstreamer as well as Gstreamer plugins,
which you probably have installed anyway. You can simple run the application
by cloning the project or downloading it and running the following terminal
commands: 
`cd path/to/mothmusicplayer/mothmusicplayer3
python __main__.py`

or you can navigate to the mothmusicplayer directory and do:
`pip install mothmusicplayer3` so you can start the application by
simply calling `mothmusicplayer3` from terminal.

*Marco Hrlic*
