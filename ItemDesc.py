#!/usr/bin/env python3
# coding=utf8
import codecs
import fnmatch
import json
import os
import sys
from collections import OrderedDict

if len(sys.argv) < 2:
    sys.exit(os.EX_NOINPUT)

dir = sys.argv[1]

FS3 = dict()
FS4 = dict()

explain_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_*.txt')
]

explain_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_Actor_*.txt')
]

explain_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_SkillRing.txt')
]

explain_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Explain_System.txt')
]

explain_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Items_Leftovers.txt')
]

explain4_files = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_Stack_Gat*.txt')
]

explain4_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_Stack_Orderitem.txt')
]

explain4_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_QuestTrigger.txt')
]

explain4_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_Stack_RingL.txt')
]

explain4_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_Stack_Music.txt')
]

explain4_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_Stack_RingR.txt')
]

explain4_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_AvatarWPN_*.txt')
]

explain4_files += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Item_AvatarWPN_*.txt')
]

explain3_files = [x for x in explain_files if x not in explain4_files]

for files in explain3_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        for entry in djson:
            if (entry["tr_text"] != ""):
                t = entry["tr_text"]
            else:
                t = entry["jp_text"]
            FS3[t] = len(entry["tr_explain"].rstrip().split('\n'))

FS3k = OrderedDict(sorted(FS3.items(), key=lambda t: t[0]))
FS3s = OrderedDict(sorted(FS3k.items(), key=lambda t: t[1]))

for e in FS3s:
    if FS3[e] > 3:
        print("Item Desc '{}' is too big: {}".format(e, FS3[e]))

for files in explain4_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        for entry in djson:
            if (entry["tr_text"] != ""):
                t = entry["tr_text"]
            else:
                t = entry["jp_text"]
            FS4[t] = len(entry["tr_explain"].rstrip().split('\n'))

FS4k = OrderedDict(sorted(FS4.items(), key=lambda t: t[0]))
FS4s = OrderedDict(sorted(FS4k.items(), key=lambda t: t[1]))

for e in FS4s:
    if FS4[e] > 4:
        print("Item Desc '{}' is too big: {}".format(e, FS4[e]))

