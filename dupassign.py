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

blacklist = list()
json_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, '*.txt')
]

#  Name_Actor_Enemy.txt
blacklist += ["DragonMagmaEx"]
#  UI_Server.txt
blacklist += ["313_t", "400_t", "221_t"]
blacklist += ["313_b", "400_b", "221_b"]
#  ChipExplain_ActiveExplain.txt
blacklist += ["72060"]
#  Name_Chip_ActiveName.txt
blacklist += ["72020"]
#  Name_UICharMake_AccessoryName.txt
blacklist += ["No06421"]
blacklist += ["No14429"]
blacklist += ["No00090"]

for files in json_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        assigns = dict()
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
                if a not in blacklist:
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
