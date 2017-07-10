#!/usr/bin/env python3
# coding=utf8
import codecs
import re
import os
# import pprint
import simplejson
import sys

countdup = 0
bufout = "FILE: ID"
os.chdir(os.getcwd() + "/json")
ENMap = dict()
json_files = [f for f in os.listdir('./') if re.match(r'Item_.*\.txt', f)]
for files in json_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        try:
            djson = simplejson.load(json_file)
            for rmid in djson:
                if (("tr_text" in rmid) and (rmid["tr_text"] != "")):
                    # print(rmid["tr_text"])
                    if rmid["tr_text"] not in ENMap:
                        ENMap[rmid["tr_text"]] = rmid["jp_text"]
                    elif ENMap[rmid["tr_text"]] == rmid["jp_text"]:
                        print("DUP")
                    else:
                        bufout += ("\n%s: %s DUP name" % (files, rmid["assign"]))
                        countdup += 1
                    if "’" in rmid["tr_text"]:
                        bufout += ("\n%s: %s ’ in %s" % (files, rmid["assign"],rmid["tr_text"]))
                        countdup += 1
        except ValueError as e:
            print("%s: %s") % (files, e)

if countdup != 0:
    sys.exit(bufout)
