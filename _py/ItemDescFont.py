#!/usr/bin/env python3
# coding=utf8
import _fonts
import codecs
from collections import OrderedDict
import fnmatch
import json
import multiprocessing as mp
import os
import sys

linelimit = 32.00


def word_wrap(string, width=00.00):
    words = string.replace("\n", "  ").split(" ")
    newstrings = []
    current = ""
    wordi = 0

    while True:
        current = ""
        lastgood = ""

        if len(words) == wordi:
            break

        while len(words) > wordi:
            current = current

            if (current == ""):
                current += words[wordi]
            else:
                current += " " + words[wordi]

            if (_fonts.textlength(current) >= width):
                break

            lastgood = current
            wordi += 1

        if (lastgood == "" and len(words) > wordi):
            lastgood = words[wordi]
            wordi += 1

        if (lastgood != ""):
            newstrings.append(lastgood)

    warped = "\n".join(newstrings)

    warpeds = warped.replace("\n", " ").split(" ")

    if words == warpeds:
        return warped
    else:
        print(words)
        print(warpeds)

    return ""


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out


def check(filename):
    f = os.path.splitext(os.path.basename(filename))[0]
    with codecs.open(filename, mode='r', encoding='utf-8') as json_file:
        djson = json.load(json_file)
        update = False
        for entry in djson:
            tt = entry["tr_text"]
            jt = entry["jp_text"]
            te = entry["tr_explain"]
            je = entry["jp_explain"]
            if tt == "":
                t = jt
            else:
                t = tt
            if te == "" or je == te:
                continue
            ce = remove_html_markup(te)
            fc = "{}:{}:{}".format(f, t, ce)
            FS[fc] = _fonts.textlength(ce)
            if (FS[fc] >= linelimit):
                ww = word_wrap(ce, linelimit)
                if (ww == ""):
                    FS[fc] = 1000
                elif te == ce:
                    FS[fc] = 0
                    fc = "{}:{}:{}".format(f, t, ww)
                    FS[fc] = _fonts.textlength(ww)
                    entry["tr_explain"] = ww
                    update = True
                else:
                    FS[fc] = 0
                    fc = "{}:{}:{}".format(f, t, ww)
                    FS[fc] = 1000 + _fonts.textlength(ce)

        if (update):
            print("Updating {}".format(filename))
            with codecs.open(filename, mode='w+', encoding='utf-8') as json_file:
                json.dump(
                    djson, json_file, ensure_ascii=False,
                    indent="\t", sort_keys=False)
                json_file.write("\n")
            return filename
    return ""


if __name__ == '__main__':
    # error counter
    counterr = 0

    # Need the json path
    if len(sys.argv) < 2:
        dir = "json"
    else:
        dir = sys.argv[1]

    manager = mp.Manager()
    FS = manager.dict()

    items_files = [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(dir)
        for f in fnmatch.filter(files, 'Item_*.txt')
    ]

    items_files += [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(dir)
        for f in fnmatch.filter(files, 'Explain_Actor_*.txt')
    ]

    items_files += [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(dir)
        for f in fnmatch.filter(files, 'Explain_SkillRing.txt')
    ]

    items_files += [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(dir)
        for f in fnmatch.filter(files, 'Explain_System.txt')
    ]

    items_files += [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(dir)
        for f in fnmatch.filter(files, 'Items_Leftovers.txt')
    ]

    if len(sys.argv) == 3 and sys.argv[2] != "0":
        _fonts.init(int(sys.argv[2]))
    else:
        _fonts.init()

    p = mp.Pool(mp.cpu_count())
    erra = p.map(check, items_files)
    p.close()
    p.join()

    FSk = OrderedDict(sorted(FS.items(), key=lambda t: t[0]))
    FSs = OrderedDict(sorted(FSk.items(), key=lambda t: t[1]))

    if len(sys.argv) == 3:
        print(json.dumps(FSs, ensure_ascii=False, indent="\t", sort_keys=False))
    else:  # JP MAX: 42.73
        FSEP = OrderedDict((key, value) for key, value in FSs.items() if (abs(value) > linelimit))
        errormsg = False
        for e, s in FSEP.items():  # MAX: 32
            s = abs(s)
            t = e.replace("\n", "\\n")
            if (s > linelimit):
                counterr += 1
            if not errormsg:
                print("--------------------------------------------------------------------------------")
                print("Items following are over the limit:")
                errormsg = True
            print("Item Desc '{}' is too long: {}".format(t, s))

    # Disable error
    # counterr = -counterr

    if counterr > 0:
        sys.exit("Issues found")
