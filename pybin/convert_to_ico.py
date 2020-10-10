#!/usr/bin/env python3

import os
from PIL import Image
import argparse
from argparse import RawTextHelpFormatter


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


class Outfstr(object):
    def __init__(self, ext):
        self.ext = ext

    def __call__(self, argstr):
        _ ,ext = os.path.splitext(argstr)
        if ext == self.ext:
            return str(argstr)
        else:
            emes = "{} doesn't match {}".format(
                                            argstr,
                                            self.ext)
            raise TypeError(emes)


def convert_png_to_ico(png_file, ico_out):
    img = Image.open(png_file)
    img.save(ico_out)


if __name__ == "__main__":
    msg = "this program convert png or jpeg to ico file"
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@",
                                formatter_class=RawTextHelpFormatter)
    ico_str = Outfstr(".ico")
    parser.add_argument("png_file", type=fnmstr, nargs="?")
    parser.add_argument("ico_out", type=ico_str, nargs="?",
                        default="./out.ico")
    args = parser.parse_args()
    PNG_FILE = args.png_file
    ICO_OUT = args.ico_out
    convert_png_to_ico(PNG_FILE, ICO_OUT)
