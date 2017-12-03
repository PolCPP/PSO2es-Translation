#!/usr/bin/env python3
# coding=utf8
import _fonts
import codecs
import fnmatch
import json
import os
import sys
from collections import OrderedDict

# error counter
counterr = 0

# Need the json path
if len(sys.argv) < 2:
    dir = "json"
else:
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


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c
    return out


for files in items_files:
    f = os.path.splitext(os.path.basename(files))[0]
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        for entry in djson:
            tt = entry["tr_text"]
            jt = entry["jp_text"]
            te = entry["tr_explain"]
            je = entry["jp_explain"]
            if tt == "":
                t = jt
            else:
                t = tt
            if te == "" or je == te:
                continue
            ce = remove_html_markup(te)
            fc = "{}:{}:{}".format(f, t, ce)
            if len(sys.argv) > 2 or sys.argv[-1] != "0":
                fc = fc.replace("\n", "\\n")
            if (fc in FS):
                continue
                print(fc)
            FS[fc] = _fonts.textlength(ce)

FSk = OrderedDict(sorted(FS.items(), key=lambda t: t[0]))
FSs = OrderedDict(sorted(FSk.items(), key=lambda t: t[1]))

if len(sys.argv) == 3:
    print(json.dumps(FSs, ensure_ascii=False, indent="\t", sort_keys=False))
else:  # JP MAX: 42.73
    FSEP = OrderedDict((key, value) for key, value in FSs.items() if value > 42.73)
    for e, s in FSEP.items():  # MAX: 33
            t = e.replace("\n", "\\n")
            counterr += 1
            print("Item Desc '{}' is too long: {}".format(t, s))

# Disable error
counterr = 0

if counterr != 0:
    sys.exit("Issues found")
