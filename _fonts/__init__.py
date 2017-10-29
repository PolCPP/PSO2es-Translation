#!/usr/bin/env python3
# coding=utf8
import os
from PIL import ImageFont


def init():
    global fontr
    font = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)
        ),
        "DF-SouGei-W7003.ttf"
    )
# "DF-SouGei-W7003.ttf"
# "DF-HeiSeiGothic-W7003.ttf"
    fontr = ImageFont.truetype(
        font=font,
        size=1
    )


def itemlength(name=""):
    global fontr
    w, h = fontr.getsize(name)
    return w
