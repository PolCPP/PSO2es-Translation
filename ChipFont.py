#!/usr/bin/env python3
# coding=utf8
import _fonts
import codecs
import fnmatch
import json
import os
import sys
from collections import OrderedDict

if len(sys.argv) < 2:
    sys.exit(os.EX_NOINPUT)

dir = sys.argv[1]

FS = dict()

chip_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_Chip_*.txt')
]

wpn_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_Weapon_*.txt')
]

wpn_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'UI_Weaponoid_Name.txt')
]

WPN = list()

if len(sys.argv) == 3 and sys.argv[2] != "0":
    _fonts.init(int(sys.argv[2]))
else:
    _fonts.init()

for files in chip_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        for entry in djson:
            t = entry["tr_text"]
            j = entry["jp_text"]
            if t == "" or j.replace("\r\n", "\n") == t:
                continue
            FS[t] = _fonts.textlength(t)

for files in wpn_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        for entry in djson:
            t = entry["tr_text"]
            j = entry["jp_text"]
            if j == "" or j == "-":
                continue
            WPN.append([j])
            if t == "" or j == t:
                continue
            WPN.append([t])

FSk = OrderedDict(sorted(FS.items(), key=lambda t: t[0]))
FSs = OrderedDict(sorted(FSk.items(), key=lambda t: t[1]))

FSWP = OrderedDict((key, value) for key, value in FSs.items() if value >= 32)

FSTL = OrderedDict((key, value) for key, value in FSWP.items() if value >= 60)

FSWPN = OrderedDict((key, value) for key, value in FSWP.items() if key not in FSTL)

FSWPNTL = OrderedDict((key, value) for key, value in FSs.items() if key in WPN)

FSER = OrderedDict()

FSER.update(FSTL)  # Bigger then 60 first
FSER.update(FSWPNTL)  # Bigger the 32 but less then 60 and in the weapon list

if len(sys.argv) == 3:
    print(json.dumps(FSER, ensure_ascii=False, indent="\t", sort_keys=False))
else:
    for e, s in FSER.items():
        print("Chip Name '{}' is too long: {}".format(e, s))
