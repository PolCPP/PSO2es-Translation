#!/usr/bin/python
# coding=utf8
import codecs
import re
import os
import simplejson
import sys

counterr = 0
invalid_json_files = []
os.chdir(os.getcwd() + "/json")
json_files = [f for f in os.listdir('.') if re.match(r'.*\.txt', f)]
for files in json_files:
    with codecs.open(files, mode='r', encoding='utf-8') as json_file:
        try:
            countin = 0
            djson = simplejson.load(json_file)
            for rmid in djson:
                countin += 1
            if (countin == 0):
               print("%s: %s") % (files, "BLANK")
               invalid_json_files.append(files)
        except ValueError as e:
            print("%s: %s"% (files, e))
            invalid_json_files.append(files)

counterr += len(invalid_json_files)
if counterr != 0:
    sys.exit("=============\nJSON files with issues: %d" % counterr)
