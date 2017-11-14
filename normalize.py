#!/usr/bin/env python3
# coding=utf8
import codecs
import fnmatch
import os
import json
import sys
import unicodedata
from collections import OrderedDict

quick = {
    "*": "＊",  # Undo normalize
    "『": "\"", "』": "\"",  # Use English Quotes
    "–": "-", "‒": "-",  # Replaces DASHs with HYPHEN-MINUS
    "​": "",  # ZERO WIDTH SPACE need to gone from this world
    "ō": "ou", "ū": "uu",  # MACRONs are not supported
    "\0": "\0"
}

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

blacklist_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_Quest_AreaName.txt')
]

bl = {"!", "＊", "†", "-", "士", "1", "2", "3", "4", "5"}


def pairr(j=None, t=None):
    if t is None:
        t = ""
    s = 0
    e = -1
    l = len(j)
    if l > 1:
        while s < (l-1) and j[s] in bl:
            s = s + 1
        yield s
        while e <= -(l-1) and j[e] in bl:
            e = e - 1
        yield e
    else:
        yield None
        yield None

    s = 0
    e = -1
    l = len(t)
    if l > 1:
        while s <= (l-1) and t[s] in bl:
            s = s + 1
        yield s
        while e <= -(l-1) and t[e] in bl:
            e = e - 1
        yield e
    else:
        yield None
        yield None


for files in json_files:
    update = False
    nk = 'NFKC'
    if files in blacklist_files:
        nk = 'NFC'
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file, object_pairs_hook=OrderedDict)
        for entry in djson:
            je = None
            for data in entry:
                if data.startswith('jp_') and False:
                    jl = data
                    tl = jl.replace("jp_", "tr_")
                    t = entry[tl]
                    j = entry[jl]
                    if t == "":
                        continue
                    js, je, ts, te = pairr(j, t)
                    if t is None and j[js:je] == t[ts:te] and t != j:
                        update = True
                        je = j
                if data.startswith('tr_'):
                    tl = data
                    jl = tl.replace("tr_", "jp_")
                    t = entry[tl]
                    j = entry[jl]
                    if t == j:
                        continue
                    if je is not None:
                        j = je
                    if t == j:
                        continue
                    if t is None:
                        continue
                    tn = unicodedata.normalize(nk, t)
                    trans = tn.maketrans(quick)
                    g = tn.translate(trans)
                    if g == t:
                        continue
                    update = True
                    entry[tl] = g

    if (update):
        print("Updating {}".format(files))
        with codecs.open(files, mode='w+', encoding='utf-8') as json_file:
            json.dump(
                djson, json_file, ensure_ascii=False,
                indent="\t", sort_keys=False)
            json_file.write("\n")

if countdup != 0:
    sys.exit("Issues found")
