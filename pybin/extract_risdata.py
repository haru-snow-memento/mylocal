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
    ex_args_grp.add_argument("--to_ris", action="store_true",
                             nargs="?", default=False)
    ex_args_grp.add_argument("--to_bib", action="store_true",
                             nargs="?", default=False)
    ex_args_grp.add_argument("--to_dois", action="store_true",
                             nargs="?", default=False)
    args = parser.parse_args()
    RISPATHS = args.rispaths
    OFILE = args.ofile
    PIDS = args.pids
    KEY = args.key
    MODE = args.mode
    TO_RIS = args.to_ris
    TO_BIB = args.to_bib
    TO_DOIS = args.to_dois
    admin_ris = AdminRISText(RISPATHS)
    if KEY is not None:
        admin_ris.write_key_values(KEY, OFILE,
                                   pids=PIDS, mode=MODE)
    elif TO_RIS:
        admin_ris.write_ris(OFILE, pids=PIDS, mode=MODE)
    elif TO_BIB:
        admin_ris.write_bib(OFILE, pids=PIDS, mode=MODE)
    elif TO_DOIS:
        admin_ris.write_dois(OFILE, pids=PIDS, mode=MODE)
    else:
        raise AssertionError("")
