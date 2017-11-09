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

items_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_*.txt')
]

items_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_Actor_*.txt')
]

items_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_SkillRing.txt')
]

items_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_System.txt')
]

items_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Items_Leftovers.txt')
]

if len(sys.argv) == 3 and sys.argv[2] != "0":
    _fonts.init(int(sys.argv[2]))
else:
    _fonts.init()

for files in items_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        for entry in djson:
            t = entry["tr_explain"]
            j = entry["jp_explain"]
            if t == "" or j == t:
                continue
            FS[t] = _fonts.textlength(t)

FSk = OrderedDict(sorted(FS.items(), key=lambda t: t[0]))
FSs = OrderedDict(sorted(FSk.items(), key=lambda t: t[1]))

if len(sys.argv) == 3:
    print(json.dumps(FSs, ensure_ascii=False, indent="\t", sort_keys=False))
else:
    for e in FSs:  # JP MAX: 48.34
        if FS[e] > 33:  # MAX: ???
            t = e.replace("\n", "<br>")
            print("Item Desc '{}' is too long: {}".format(t, FS[e]))
