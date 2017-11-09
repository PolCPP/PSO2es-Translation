#!/usr/bin/env python3
# coding=utf8
import codecs
import fnmatch
import os
import json
import sys

countdup = 0

if len(sys.argv) < 2:
    sys.exit(os.EX_NOINPUT)

dir = sys.argv[1]

json_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, '*.txt')
]

#  DragonMagmaEx
nope_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_Actor_Enemy.txt')
]

#  *_t
#  *_b
nope_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'UI_Server.txt')
]

#  72060
nope_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'ChipExplain_ActiveExplain.txt')
]

#  72020
nope_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_Chip_ActiveName.txt')
]

#  No06421
#  No14429
#  No00090
nope_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_UICharMake_AccessoryName.txt')
]

assign_files = [x for x in json_files if x not in nope_files]

for files in assign_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        assigns = dict()
        #print(files)
        for entry in djson:
            if "assign" not in entry:
                 continue
            a = entry["assign"]
            if "tr_text" in entry:
                t = entry["tr_text"]
                if t == "":
                    t = entry["jp_text"]
            elif "tr_explainShort" in entry:
                t = entry["tr_explainShort"]
                if t == "":
                    t = entry["jp_explainShort"]
            else:
                t = entry["text"]
            if a in assigns:
                print("{}: {}:{}/{}".format(
                    files,
                    a,
                    t,
                    assigns[a]
                ))
                countdup = countdup+1
            else:
                assigns[a] = t

if countdup != 0:
    sys.exit("Issues found")
