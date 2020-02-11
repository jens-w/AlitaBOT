#!/usr/bin/python3
import importlib
import modules.AlitaCommandConvert.AlitaCommandConvert

command_prefix = ["!", "."]
modules_list = {"modules.AlitaCommandConvert.AlitaCommandConvert"}

for module in modules_list:
    print("reloading " + module)
    importlib.reload(importlib.import_module(module))

commands = {"convert": modules.AlitaCommandConvert.AlitaCommandConvert.convert}
