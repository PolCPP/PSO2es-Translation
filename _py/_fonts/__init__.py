#!/usr/bin/env python3
# coding=utf8
import os
from PIL import ImageFont


def init(size=190):
    global fontr
    font = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        "DF-HeiSeiGothic-W7003.ttf"
    )
# "DF-SouGei-W7003.ttf"
# "DF-HeiSeiGothic-W7003.ttf"
    fontr = ImageFont.truetype(
        font=font,
        size=size
    )


def textlength(name=""):
    global fontr
    w = -1
    h = -1
    t = name.replace("<%br>", "\n").replace("<br>", "\n").rstrip()
    for sl in t.splitlines():
                w, h = max(fontr.getsize(sl), (w, h))
    return w/100
