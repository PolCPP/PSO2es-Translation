#!/usr/bin/env python3
# coding=utf8
import codecs
import json
import os
import regex
import shutil

json_loc = os.path.join("..", "json")

file_names = [["Accessory", "accessory"], ["BodyPaint", "body paint"],
              ["Eye", "eyes"], ["EyeBrow", "eyebrows"],
              ["EyeLash", "eyelashes"], ["FacePaint", "makeup"],
              ["Hairstyle", "hairstyle"], ["Sticker", "sticker"]]


for name in file_names:
    items_file_name = "Item_Stack_" + name[0] + ".txt"
    item_type = name[1]
    
    try:
        items_file = codecs.open(os.path.join(json_loc, items_file_name),
                                 mode = 'r', encoding = 'utf-8')
    except FileNotFoundError:
        print("\t{0} not found.".format(items_file_name))
        continue
    
    items = json.load(items_file)
    print("{0} loaded.".format(items_file_name))
    
    items_file.close()
    
    for item in items:
        if item["tr_text"] != "" and item["tr_explain"] == "":
            item["tr_explain"] = "Unlocks the "
            
            if len(regex.findall("女性のみ使用可能。", item["jp_explain"])) > 0:
                item["tr_explain"] += "female-only "
            elif len(regex.findall("男性のみ使用可能。", item["jp_explain"])) > 0:
                item["tr_explain"] += "male-only "
            
            item["tr_explain"] += (item_type + "\n\""
                                   + item["tr_text"] + "\"\n"
                                   + "for use in the Beauty Salon.")

            if len(regex.findall("着用時はインナーが非表示になります。", item["jp_explain"])) > 0:
                item["tr_explain"] += '\n<yellow>※Hides innerwear when worn.<c>'

            print("Translated description for {0}".format(item["tr_text"]))

    items_file = codecs.open(os.path.join(json_loc, items_file_name),
                             mode = 'w', encoding = 'utf-8')
    json.dump(items, items_file, ensure_ascii=False, indent="\t", sort_keys=False)
    items_file.write("\n")
    items_file.close()
