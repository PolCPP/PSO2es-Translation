#!/usr/bin/env python3
# coding=utf8
import codecs
import csv
import fnmatch
import json
import re
import os
import sys
from collections import OrderedDict

TR_name = dict()
TR_explain = dict()

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
	TR_name[k] = t
	TR_explain[k] = d.replace("\n","<br>")

json_files = [
	os.path.join(dirpath, f)
	for dirpath, dirnames, files in os.walk(dir)
	for f in fnmatch.filter(files, 'Item_*.txt')
]

for files in json_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        change = False
        try:
            djson = json.load(json_file, object_pairs_hook=OrderedDict)
            for entry in djson:
                if entry["jp_text"] in TR_name:
                    k = entry["jp_text"]
                    t = entry["tr_text"]
                    d = entry["tr_explain"].replace("<br>","\n")
                    if TR_name[k] != t and t != "":
                        TR_name[k] = t
                        change = True
                    if TR_explain[k] != d and d != "":
                        TR_explain[k] = d
                        change = True
                else:
                    k = entry["jp_text"]
                    t = entry["tr_text"]
                    d = entry["tr_explain"]
                    TR_name[k] = t
                    TR_explain[k] = d
            if change:
                print("Updating {}.txt".format(os.path.splitext(os.path.basename(files))[0]))
                djson = [
                    OrderedDict([('assign', e["assign"]), ('jp_text', e["jp_text"]), ('tr_text', TR_name[e["jp_text"]]), ('jp_explain', e['jp_explain']), ('tr_explain', TR_explain[e["jp_text"]])])
                    for e in djson
                ]
                with codecs.open(files, mode='w+', encoding='utf-8') as json_file:
                    json.dump(djson, json_file, ensure_ascii=False, indent="\t", sort_keys=False)
                    json_file.write("\n")
        except ValueError as e:
            print("%s: %s" % (files, e))
