#!/usr/bin/python3
import re
import AlitaGeneralTools


def convert(name, text):
    text = AlitaGeneralTools.double_spaces_to_single_space(text)
    text = AlitaGeneralTools.remove_starting_space(text)
    error_nan = name + ": not a number: "
    error_notastring = name + ": not a string: "
    error_arguments = name + ": cannot parse arguments: " + text

    if text.find(" ") > 0:
        split = text.split(" ")

        if len(split) == 2:
            how_many = get_number(split[0])

            if how_many == "error":
                return error_nan + split[0]

            how_many = float(how_many)
            what = get_text(split[0])

            if what == "error":
                what = get_text(split[1])

                if what == "error" or str(what) != str(split[1]):
                    return error_notastring + split[1]

                return name + ": " + convert_what_to_what(how_many, what)

            to_what = get_text(split[1])

            if to_what == "error" or str(to_what) != str(split[1]):
                return error_notastring + split[1]

            return name + ": " + convert_what_to_what(how_many, what, to_what)

        if len(split) == 3:
            how_many = get_number(split[0])

            if how_many == "error" or float(how_many) != float(split[0]):
                return error_nan + split[0]

            how_many = float(how_many)
            what = get_text(split[1])

            if what == "error" or str(what) != str(split[1]):
                return error_notastring + split[1]

            to_what = get_text(split[2])

            if to_what == "error" or str(to_what) != str(split[2]):
                return error_notastring + split[2]

            return name + ": " + convert_what_to_what(how_many, what, to_what)

        return error_arguments

    how_many = get_number(text)

    if how_many == "error":
        return error_nan + text

    how_many = float(how_many)
    what = get_text(text)

    if what == "error":
        return error_notastring + text

    return name + ": " + convert_what_to_what(how_many, what)


def get_number(text):
    regex = re.compile(r"\d+(?:\.\d+)?")
    regex_result = regex.findall(text)

    if len(regex_result) != 1:
        return "error"
    else:
        return regex_result[0]


def get_text(text):
    regex = re.compile(r"[a-z]+", re.IGNORECASE)
    regex_result = regex.findall(text)

    if len(regex_result) != 1:
        return "error"
    else:
        return regex_result[0]


def convert_what_to_what(how_many, what, to_what=""):
    what = what.lower()

    if to_what != "":
        to_what = to_what.lower()

    fahrenheit = {"f", "fahrenheit", "°f"}
    celsius = {"c", "celsius", "°c"}

    if what in fahrenheit:
        if to_what in celsius or to_what == "":
            return str((how_many - 32) * (5 / 9)) + "°C"

        return "wrong argument: " + to_what

    if what in celsius:
        if to_what in fahrenheit or to_what == "":
            return str((how_many * (9 / 5)) + 32) + "°F"

        return "wrong argument: " + to_what

    mile = {"mile", "miles"}
    kilometre = {"km", "kilometre", "kilometres", "kilometer", "kilometers"}
    metre = {"m", "metre", "metres", "meter", "meters"}
    centimetre = {"cm", "centimetre", "centimetres", "centimeter", "centimeters"}
    millimetre = {"mm", "millimetre", "millimetres", "millimeter", "millimeters"}
    yard = {"yard", "yards"}
    foot = {"foot", "feet"}
    inch = {"inch", "inches"}

    if what in mile:
        if to_what == "":
            to_what = "km"

        if to_what in kilometre:
            return str(how_many * 1.60934) + " kilometres"

        if to_what in metre:
            return str(1000 * how_many * 1.60934) + " metres"

        if to_what in centimetre:
            return str(100000 * how_many * 1.60934) + " centimetres"

        if to_what in millimetre:
            return str(1000000 * how_many * 1.60934) + " millimetres"

        if to_what in yard:
            return str(how_many * 1760) + " yards"

        if to_what in foot:
            return str(how_many * 5280) + " feet"

        if to_what in inch:
            return str(how_many * 63360) + " inches"

        return "wrong argument: " + to_what

    if what in kilometre:
        if to_what == "":
            to_what = "mile"

        if to_what in mile:
            return str(how_many / 1.60934) + " miles"

        if to_what in metre:
            return str(how_many * 1000) + " metres"

        if to_what in centimetre:
            return str(how_many * 100000) + " centimetres"

        if to_what in millimetre:
            return str(how_many * 1000000) + " millimetres"

        if to_what in yard:
            return str(how_many * 1094) + " yards"

        if to_what in foot:
            return str(how_many * 3281) + " feet"

        if to_what in inch:
            return str(how_many * 39370) + " inches"

        return "wrong argument: " + to_what

    if what in metre:
        if to_what == "":
            to_what = "yard"

        if to_what in mile:
            return str(how_many / 1609) + " miles"

        if to_what in kilometre:
            return str(how_many / 1000) + " kilometres"

        if to_what in centimetre:
            return str(how_many * 100) + " centimetres"

        if to_what in millimetre:
            return str(how_many * 1000) + " millimetres"

        if to_what in yard:
            return str(how_many * 1.094) + " yards"

        if to_what in foot:
            return str(how_many * 3.281) + " feet"

        if to_what in inch:
            return str(how_many * 39.37) + " inches"

        return "wrong argument: " + to_what

    if what in centimetre:
        if to_what == "":
            to_what = "inch"

        if to_what in mile:
            return str(how_many / 160934) + " miles"

        if to_what in kilometre:
            return str(how_many / 100000) + " kilometres"

        if to_what in millimetre:
            return str(how_many * 10) + " millimetres"

        if to_what in yard:
            return str(how_many / 91.44) + " yards"

        if to_what in foot:
            return str(how_many / 30.48) + " feet"

        if to_what in inch:
            return str(how_many / 2.54) + " inches"

        return "wrong argument: " + to_what

    if what in millimetre:
        if to_what == "":
            to_what = "inch"

        if to_what in mile:
            return str(how_many / 1609000) + " miles"

        if to_what in kilometre:
            return str(how_many / 1000000) + " kilometres"

        if to_what in metre:
            return str(how_many / 1000) + " metres"

        if to_what in centimetre:
            return str(how_many / 10) + " centimetres"

        if to_what in yard:
            return str(how_many / 914) + " yards"

        if to_what in foot:
            return str(how_many / 305) + " feet"

        if to_what in inch:
            return str(how_many / 25.4) + " inches"

        return "wrong argument: " + to_what

    if what in yard:
        if to_what == "":
            to_what = "metre"

        if to_what in mile:
            return str(how_many / 1760) + " miles"

        if to_what in kilometre:
            return str(how_many / 1094) + " kilometres"

        if to_what in metre:
            return str(how_many / 1094 / 1000) + " metres"

        if to_what in centimetre:
            return str(how_many * 91.44) + " centimetres"

        if to_what in millimetre:
            return str(how_many * 914) + " millimetres"

        if to_what in foot:
            return str(how_many * 3) + " feet"

        if to_what in inch:
            return str(how_many * 36) + " inches"

        return "wrong argument: " + to_what

    if what in foot:
        if to_what == "":
            to_what = "cm"

        if to_what in mile:
            return str(how_many / 5280) + " miles"

        if to_what in kilometre:
            return str(how_many / 3281) + " kilometres"

        if to_what in metre:
            return str(how_many / 3281 / 1000) + " metres"

        if to_what in centimetre:
            return str(how_many * 30.48) + " centimetres"

        if to_what in millimetre:
            return str(how_many * 304.8) + " millimetres"

        if to_what in yard:
            return str(how_many / 3) + " yards"

        if to_what in inch:
            return str(how_many * 12) + " inches"

        return "wrong argument: " + to_what

    if what in inch:
        if to_what == "":
            to_what = "cm"

        if to_what in mile:
            return str(how_many / 63360) + " miles"

        if to_what in kilometre:
            return str(how_many / 39370) + " kilometres"

        if to_what in metre:
            return str(how_many / 39.37) + " metres"

        if to_what in centimetre:
            return str(how_many * 2.54) + " centimetres"

        if to_what in millimetre:
            return str(how_many * 25.4) + " millimetres"

        if to_what in yard:
            return str(how_many / 36) + " yards"

        if to_what in foot:
            return str(how_many / 12) + " feet"

        return "wrong argument: " + to_what

    tonne = {"tonne", "metricton"}
    kilogram = {"kg", "kilogram"}
    gram = {"g","gr", "gram"}
    milligram = {"mg", "milligram"}
    imperial_ton = {"imperialton"}
    us_ton = {"uston"}
    stone = {"stone", "st"}
    pound = {"pound", "lb"}
    ounce = {"ounce", "oz"}

    if what in tonne:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in kilogram:
            return str(how_many * 1000) + " kilogram"

        if to_what in gram:
            return str(how_many * 1000 * 1000) + " gram"

        if to_what in milligram:
            return str(how_many * 1000 * 1000 * 1000) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 1.0160) + " imperial ton"

        if to_what in us_ton:
            return str(how_many * 1.102) + " US ton"

        if to_what in stone:
            return str(how_many * 157) + " stone"

        if to_what in pound:
            return str(how_many * 2205) + " pound"

        if to_what in ounce:
            return str(how_many * 35274) + " ounce"

        return "wrong argument: " + to_what

    if what in kilogram:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many / 1000) + " tonne"

        if to_what in gram:
            return str(how_many * 1000) + " gram"

        if to_what in milligram:
            return str(how_many * 1000 * 1000) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 1016) + " imperial ton"

        if to_what in us_ton:
            return str(how_many / 907) + " US ton"

        if to_what in stone:
            return str(how_many / 6.35) + " stone"

        if to_what in pound:
            return str(how_many * 2.205) + " pound"

        if to_what in ounce:
            return str(how_many * 35.274) + " ounce"

        return "wrong argument: " + to_what

    if what in gram:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many / 1000 / 1000) + " tonne"

        if to_what in kilogram:
            return str(how_many / 1000) + " kilogram"

        if to_what in milligram:
            return str(how_many * 1000) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 1016 / 1000) + " imperial ton"

        if to_what in us_ton:
            return str(how_many / 907 /  1000) + " US ton"

        if to_what in stone:
            return str(how_many / 6350) + " stone"

        if to_what in pound:
            return str(how_many / 454) + " pound"

        if to_what in ounce:
            return str(how_many / 28.35) + " ounce"

        return "wrong argument: " + to_what

    if what in milligram:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many / 1000 / 1000 / 1000) + " tonne"

        if to_what in kilogram:
            return str(how_many / 1000 / 1000) + " kilogram"

        if to_what in gram:
            return str(how_many / 1000) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 1016 / 1000 / 1000) + " imperial ton"

        if to_what in us_ton:
            return str(how_many / 907 / 1000 / 1000) + " US ton"

        if to_what in stone:
            return str(how_many / 6350 / 1000) + " stone"

        if to_what in pound:
            return str(how_many / 453592) + " pound"

        if to_what in ounce:
            return str(how_many / 28350) + " ounce"

        return "wrong argument: " + to_what

    if what in imperial_ton:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many * 1.016) + " tonne"

        if to_what in kilogram:
            return str(how_many * 1016) + " kilogram"

        if to_what in gram:
            return str(how_many * 1016 * 1000) + " gram"

        if to_what in milligram:
            return str(how_many * 1016 * 1000 * 1000) + " milligram"

        if to_what in us_ton:
            return str(how_many * 1.12) + " US ton"

        if to_what in stone:
            return str(how_many * 160) + " stone"

        if to_what in pound:
            return str(how_many * 2240) + " pound"

        if to_what in ounce:
            return str(how_many * 35840) + " ounce"

        return "wrong argument: " + to_what

    if what in us_ton:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many / 1.102) + " tonne"

        if to_what in kilogram:
            return str(how_many * 907) + " kilogram"

        if to_what in gram:
            return str(how_many * 907185) + " gram"

        if to_what in milligram:
            return str(how_many * 907185 * 1000) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 1.12) + " imperial ton"

        if to_what in stone:
            return str(how_many * 143) + " stone"

        if to_what in pound:
            return str(how_many * 2000) + " pound"

        if to_what in ounce:
            return str(how_many * 32000) + " ounce"

        return "wrong argument: " + to_what

    if what in stone:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many / 157) + " tonne"

        if to_what in kilogram:
            return str(how_many * 6.35) + " kilogram"

        if to_what in gram:
            return str(how_many * 6350) + " gram"

        if to_what in milligram:
            return str(how_many * 6350 * 1000) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 160) + " imperial ton"

        if to_what in us_ton:
            return str(how_many / 143) + " US ton"

        if to_what in pound:
            return str(how_many * 14) + " pound"

        if to_what in ounce:
            return str(how_many * 224) + " ounce"

        return "wrong argument: " + to_what

    if what in pound:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many / 2205) + " tonne"

        if to_what in kilogram:
            return str(how_many / 2.205) + " kilogram"

        if to_what in gram:
            return str(how_many * 454) + " gram"

        if to_what in milligram:
            return str(how_many * 453592) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 2240) + " imperial ton"

        if to_what in us_ton:
            return str(how_many / 2000) + " US ton"

        if to_what in stone:
            return str(how_many * 14) + " stone"

        if to_what in ounce:
            return str(how_many * 16) + " ounce"

        return "wrong argument: " + to_what

    if what in ounce:
        if to_what == "":
            return "don't know what to convert to"

        if to_what in tonne:
            return str(how_many / 35274) + " tonne"

        if to_what in kilogram:
            return str(how_many / 35.274) + " kilogram"

        if to_what in gram:
            return str(how_many * 28.35) + " gram"

        if to_what in milligram:
            return str(how_many * 28350) + " milligram"

        if to_what in imperial_ton:
            return str(how_many / 35840) + " imperial ton"

        if to_what in us_ton:
            return str(how_many / 32000) + " US ton"

        if to_what in stone:
            return str(how_many / 224) + " stone"

        if to_what in pound:
            return str(how_many / 16) + " pound"

        return "wrong argument: " + to_what

    return "wrong argument: " + what
