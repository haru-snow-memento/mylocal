#!/usr/bin/env python3

# formal lib
from help_bib import AdminBibText
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
    parser.add_argument("bibpaths", type=fnmstr, nargs="+")
    parser.add_argument("--ofile", type=str, nargs="?", default=None)
    parser.add_argument("--pids", type=int, nargs="+", default=None)
    parser.add_argument("--mode", type=str, nargs="?",
                        default="w", choices=["w", "a"])
    ex_args_grp = parser.add_mutually_exclusive_group(required=True)
    ex_args_grp.add_argument("--out_doi", action="store_true",
                             default=False)
    ex_args_grp.add_argument("--out_pbib", action="store_true",
                             default=False)
    ex_args_grp.add_argument("--out_authers", action="store_true",
                             default=False)
    args = parser.parse_args()
    BIBPATHS = args.bibpaths
    OFILE = args.ofile
    PIDS = args.pids
    MODE = args.mode
    OUT_DOI = args.out_doi
    OUT_PBIB = args.out_pbib
    OUT_AUTHERS = args.out_authers
    adminbib = AdminBibText(BIBPATHS)
    if OUT_DOI:
        adminbib.write_dois(OFILE, PIDS, mode=MODE)
    elif OUT_PBIB:
        adminbib.write_bib(OFILE, PIDS, mode=MODE)
    elif OUT_AUTHERS:
        adminbib.write_authers(OFILE, PIDS, mode=MODE)
    else:
        raise AssertionError("")
