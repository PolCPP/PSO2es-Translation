#!/usr/bin/python
import os
import simplejson
import sys

invalid_json_files = []
read_json_files = []
os.chdir(os.getcwd() + "/json")
for files in os.listdir(os.getcwd()):
    with open(files) as json_file:
        try:
            simplejson.load(json_file)
            read_json_files.append(files)
        except ValueError, e:
            print ("JSON object issue: %s") % e
            print files
            invalid_json_files.append(files)

if len(invalid_json_files) != 0:
    print invalid_json_files, len(read_json_files)
    sys.exit("Found Errors in JSON files")

