#!/usr/bin/python3
import AlitaCommandConvert

import importlib


modules = {"AlitaCommandConvert", "AlitaGeneralTools"}

for module in modules:
    importlib.reload(importlib.import_module(module))

command_prefix = {"!", "."}
commands = {"convert": AlitaCommandConvert.convert}
