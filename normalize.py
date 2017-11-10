#!/usr/bin/env python3
# coding=utf8
import codecs
import fnmatch
import os
import json
import sys
import unicodedata
from collections import OrderedDict

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


for files in json_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file, object_pairs_hook=OrderedDict)
        for entry in djson:
            for data in entry:
                if data.startswith('tr_'):
                    s = entry[data]
                    t = unicodedata.normalize('NFKD', s)
                    g = t.replace("*", "＊")
                    entry[data] = g
    with codecs.open(files, mode='w+', encoding='utf-8') as json_file:
        json.dump(
            djson, json_file, ensure_ascii=False, indent="\t", sort_keys=False)
        json_file.write("\n")

if countdup != 0:
    sys.exit("Issues found")
