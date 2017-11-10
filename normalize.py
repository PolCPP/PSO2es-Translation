#!/usr/bin/env python3
# coding=utf8
import codecs
import fnmatch
import os
import json
import sys
import unicodedata
from collections import OrderedDict

strmap = {"*": "＊", "『": "\"", "』": "\""}

# error counter
countdup = 0

# Need the json path
if len(sys.argv) < 2:
    print("Where the json folder?")
    sys.exit(os.EX_NOINPUT)

# Keep folder string
dir = sys.argv[1]

# collect all the JSON files
json_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, '*.txt')
]

blacklist_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'UI_Text.txt')
]

json_files = [x for x in json_files if x not in blacklist_files]

# build up blacklist
bl = dict()
for files in json_files:
    f = os.path.splitext(os.path.basename(files))[0]
    bl[f] = list()

#  Item_Stack_DeviceHT, Kyubey is EVIL
bl["Item_Stack_DeviceHT"] += ["Requires a Lv.100+ mag to use.\nEvolves your mag into a\nKyubey.\nContract? ／人●ω●人＼"]


for files in json_files:
    update = False
    f = os.path.splitext(os.path.basename(files))[0]
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file, object_pairs_hook=OrderedDict)
        for entry in djson:
            for data in entry:
                if data.startswith('tr_'):
                    d = data
                    j = d.replace("tr_", "jp_")
                    s = entry[d]
                    if s == entry[j]:
                        continue
                    if s in bl[f]:
                        continue
                    t = unicodedata.normalize('NFKD', s)
                    trans = t.maketrans(strmap)
                    g = t.translate(trans)
                    if g != s:
                        update = True
                    entry[d] = g
    if (update):
        print("Updating {}".format(files))
        with codecs.open(files, mode='w+', encoding='utf-8') as json_file:
            json.dump(
                djson, json_file, ensure_ascii=False,
                indent="\t", sort_keys=False)
            json_file.write("\n")

if countdup != 0:
    sys.exit("Issues found")
