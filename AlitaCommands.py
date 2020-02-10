#!/usr/bin/python3
def convert(name, text):
    return name + ": convert"


def remind(name, text):
    return name + ": remind"


command_prefix = {"!", "."}
commands = {"convert": convert, "remind": remind}
