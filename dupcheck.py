#!/usr/bin/env python3
# coding=utf8
import codecs
import fnmatch
import os
# import pprint
import json
import sys

countdup = 0
bufout = "FILE: ID\n"
ENMap = dict()

dir = os.getcwd() + "/json"

json_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_*.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_Actor_*.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_SkillRing.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_System.txt')
]

json_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_Actor_MagName.txt')
]

for files in json_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        try:
            djson = json.load(json_file)
            for rmid in djson:
                if (("tr_text" in rmid) and (rmid["tr_text"] != "")):
                    if rmid["tr_text"] not in ENMap:
                        ENMap[rmid["tr_text"]] = rmid["jp_text"]
                    elif ENMap[rmid["tr_text"]] != rmid["jp_text"]:
                        bufout += ("{}:{} {} wants the mapping of {}\n".format(
                            os.path.splitext(os.path.basename(files))[0],
                            rmid["assign"], rmid["jp_text"], rmid["tr_text"]))
                        countdup += 1
        except ValueError as e:
            print("%s: %s") % (files, e)

if countdup != 0:
    sys.exit(bufout)
