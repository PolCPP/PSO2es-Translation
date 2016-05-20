#!/usr/bin/python
import os
import simplejson
import sys

invalid_json_files = []
os.chdir(os.getcwd() + "/json")
for files in os.listdir(os.getcwd()):
    with open(files) as json_file:
        try:
            simplejson.load(json_file)
        except ValueError, e:
            print ("%s: %s") % (files, e)
            invalid_json_files.append(files)

if len(invalid_json_files) != 0:
    sys.exit("=============\nJSON files with issues: %d" % len(invalid_json_files))

