#!/usr/bin/env python

import configparser
import os


def file_path():
    return os.path.split(os.path.abspath(__file__))[0] + '/config.cfg'


def get_sections():
    config = configparser.RawConfigParser()
    with open(file_path(), 'r') as configfile:
        config.readfp(configfile)

    return config.sections()


def get_options(section):
    path = file_path()
    config = configparser.RawConfigParser()
    with open(path, 'r') as configfile:
        config.readfp(configfile)
    return config.options(section)


def get_conf(section, option, mode="bool"):
    config = configparser.RawConfigParser()
    # config.read(os.path.abspath(os.getcwd() + "/config.cfg"))

    #debug
    #print "config file path: " + os.path.abspath(os.getcwd() + "/config.cfg")

    with open(file_path(), 'r') as configfile:
        config.readfp(configfile)

    #debug
    #print config.items

    if mode == "bool":
        conf = config.getboolean(section, option)
    elif mode == "int":
        conf = config.getint(section, option)
    elif mode == "string":
        conf = config.get(section, option)
    return conf


def set_conf(section, option, value):
    config = configparser.RawConfigParser()
    config.read(file_path())
    # config.add_section(section)
    config.set(section, option, value)
    with open(file_path(), "w") as configfile:
        config.write(configfile)
        configfile.close()
		
