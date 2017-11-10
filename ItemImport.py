#!/usr/bin/env python3
# coding=utf8
import codecs
import csv
import fnmatch
import json
import os
import sys
from collections import OrderedDict

TR_name = dict()
TR_dup = dict()
TR_explain = dict()
TR_src = dict()

csv.register_dialect('pipes', delimiter='|', quoting=csv.QUOTE_NONE)

if len(sys.argv) < 3:
    sys.exit(os.EX_NOINPUT)

dir = sys.argv[1]
with open(sys.argv[2]) as f:
    CSV = list(csv.reader(f, dialect='pipes', strict=True))

for line in CSV:
    k = line[0]
    t = line[1]
    d = line[2]
    if (k == t):
        t = ""
    if k in TR_name:
        print("Item JP name {} already in".format(k))
    if t != "":
        if t in TR_dup:
            print("Item JP name {} already taken {}".format(TR_dup[t], t))
    TR_dup[t] = k
    TR_name[k] = t
    if d != "" and k in TR_explain:
        if d != TR_explain[k]:
            print("Item Desc {}/{}".format(k, t))
        elif d != TR_explain[k]:
            TR_explain[k] = d.replace(
                "<br>", "\n").rstrip().replace("\n", "<br>")
    else:
        TR_explain[k] = d.replace("<br>", "\n").rstrip().replace("\n", "<br>")
    if TR_explain[k].count("<br>") >= 4:
        print("item Desc {} is too long".format(k))
        TR_explain[k] = ""
    TR_src[k] = "CSV"

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

names_file = [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_Actor_MagName.txt')
]

names_file += [
    os.path.join(dirpath, f)
    for dirpath, dirnames, files in os.walk(dir)
    for f in fnmatch.filter(files, 'Name_UICharMake_*.txt')
]

for files in explain_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        change = False
        try:
            djson = json.load(json_file, object_pairs_hook=OrderedDict)
            for entry in djson:
                if (
                    entry["jp_text"] in TR_name and
                    TR_src[entry["jp_text"]] == "CSV"
                ):
                    k = entry["jp_text"]
                    t = entry["tr_text"]
                    d = entry["tr_explain"]
                    c = d.rstrip().replace("\n", "<br>")
                    if TR_name[k] != t and TR_name[k] != "":
                        print("TR name of \'{}\' from \'{}\' to \'{}\'".format(
                            k, t, TR_name[k]))
                        change = True
                    else:
                        TR_name[k] = t
                    if TR_explain[k] != c and TR_explain[k] != "":
                        print("TR desc of \'{}\' from \'{}\' to \'{}\'".format(
                             k, c, TR_explain[k]))
                        change = True
                    else:
                        TR_explain[k] = d
                    TR_src[k] = "JSON"
                else:
                    k = entry["jp_text"]
                    t = entry["tr_text"]
                    d = entry["tr_explain"]
                    TR_name[k] = t
                    TR_explain[k] = d
                    TR_src[k] = "NEW"
            if change:
                print("Updating {}.txt".format(
                    os.path.splitext(os.path.basename(files))[0]))
                djson = [
                    OrderedDict([
                        ('assign', e["assign"]),
                        ('jp_text', e["jp_text"]),
                        ('tr_text', TR_name[e["jp_text"]]),
                        ('jp_explain', e['jp_explain']),
                        ('tr_explain', TR_explain[e["jp_text"]].replace(
                            "<br>", "\n").rstrip())
                    ])
                    for e in djson
                ]
                with codecs.open(
                    files, mode='w+', encoding='utf-8'
                ) as json_file:
                    json.dump(
                        djson, json_file, ensure_ascii=False,
                        indent="\t", sort_keys=False)
                    json_file.write("\n")
        except ValueError as e:
            print("%s: %s" % (files, e))

for files in names_file:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        change = False
        try:
            djson = json.load(json_file, object_pairs_hook=OrderedDict)
            for entry in djson:
                if (
                    entry["jp_text"] in TR_name and
                    TR_src[entry["jp_text"]] == "CSV"
                ):
                    k = entry["jp_text"]
                    t = entry["tr_text"]
                    if TR_name[k] != t and TR_name[k] != "":
                        print("TR name of \'{}\' from \'{}\' to \'{}\'".format(
                            k, t, TR_name[k]))
                        change = True
                    else:
                        TR_name[k] = t
                    TR_src[k] = "JSON"
                else:
                    k = entry["jp_text"]
                    t = entry["tr_text"]
                    TR_name[k] = t
                    TR_src[k] = "NEW"
            if change:
                print("Updating {}.txt".format(
                    os.path.splitext(os.path.basename(files))[0]))
                djson = [
                        OrderedDict(
                            [
                                ('assign', e["assign"]),
                                ('jp_text', e["jp_text"]),
                                ('tr_text', e["tr_text"].replace(
                                    "<br>", "\n").rstrip())
                            ]
                        )
                        for e in djson
                ]
                with codecs.open(
                        files, mode='w+', encoding='utf-8'
                        ) as json_file:
                    json.dump(
                        djson, json_file, ensure_ascii=False,
                        indent="\t", sort_keys=False
                        )
                    json_file.write("\n")
        except ValueError as e:
            print("%s: %s" % (files, e))

others = list()

for e in TR_src:
    if TR_src[e] == "CSV":
        others.append(e)

others = sorted(others)

ojson = list()

for e in others:
    ojson += [
        OrderedDict(
            [
                ('jp_text', e),
                ('tr_text', TR_name[e]),
                ('jp_explain', ""),
                ('tr_explain', TR_explain[e].replace("<br>", "\n"))
            ]
        )
    ]

with codecs.open(
        os.path.join(dir, "Items_Leftovers.txt"), mode='w+', encoding='utf-8'
        ) as json_file:
    json.dump(
        ojson, json_file, ensure_ascii=False, indent="\t", sort_keys=False)
    json_file.write("\n")
