#!/usr/bin/env python3
# coding=utf8
import __init__ as _fonts
import codecs
import fnmatch
import json
import os
import sys
import unicodedata
from collections import OrderedDict

FS = dict()

_fonts.init()

for char in range(0x0, 0xFFFF):
     #print("{}".format(chr(char)))
     chard = unicodedata.name("{}".format(chr(char)), "UNKNOWN")
     if chard == "UNKNOWN":
         chard = "{}".format(hex(char))
     FS[chard] = _fonts.itemlength(chr(char))

FSk = OrderedDict(sorted(FS.items(), key=lambda t: t[0]))
FSs = OrderedDict(sorted(FSk.items(), key=lambda t: t[1]))

print(json.dumps(FSs, ensure_ascii=False, indent="\t", sort_keys=False))
