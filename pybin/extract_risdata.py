#!/usr/bin/env python3

# formal lib
from help_ris import AdminRISText
import argparse
from argparse import RawTextHelpFormatter
import os
# my lib


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


if __name__ == "__main__":
    msg = "this program extract multiple pieces of doi data."
    parser = argparse.ArgumentParser(
                                description=msg,
                                formatter_class=RawTextHelpFormatter,
                                fromfile_prefix_chars="@")
    parser.add_argument("rispaths", type=fnmstr, nargs="+")
    parser.add_argument("--ofile", type=str, nargs="?", default=None)
    parser.add_argument("--pids", type=int, nargs="+", default=None)
    parser.add_argument("--mode", type=str, nargs="?", default="w",
                        choices=["w", "a"])
    ex_args_grp = parser.add_mutually_exclusive_group(required=True)
    ex_args_grp.add_argument("--key", type=str, nargs="?", default=None)
    ex_args_grp.add_argument("--")
    args = parser.parse_args()
    RISPATHS = args.rispaths
    OFILE = args.ofile
    PIDS = args.pids
    KEY = args.key
    MODE = args.mode
    admin_ris = AdminRISText(RISPATHS)
    admin_ris.write_key_values(KEY, OFILE,
                               pids=PIDS, mode=MODE)
