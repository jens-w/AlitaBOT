#!/usr/bin/python3


def double_spaces_to_single_space(text):
    if text.find("  ") != -1:
        text = text.replace("  ", " ")
        return double_spaces_to_single_space(text)

    return text


def remove_starting_space(text):
    if text.startswith(" "):
        text = text.replace(" ", "", 1)
        return remove_starting_space(text)

    return text
