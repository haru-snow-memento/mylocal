#!/usr/bin/env python3

# formal lib
from help_bibtxt import AdminBibText
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
    parser.add_argument("bibpath", type=fnmstr, nargs="?")
    parser.add_argument("--ofile", type=str, nargs="?", default=None)
    parser.add_argument("--pids", type=int, nargs="+", default=None)
    ex_args_grp = parser.add_mutually_exclusive_group(required=True)
    ex_args_grp.add_argument("--out_doi", action="store_true",
                             default=False)
    ex_args_grp.add_argument("--out_pbib", action="store_true",
                             default=False)
    ex_args_grp.add_argument("--out_authers", action="store_true",
                             default=False)
    args = parser.parse_args()
    BIBPATH = args.bibpath
    OFILE = args.ofile
    PIDS = args.pids
    OUT_DOI = args.out_doi
    OUT_PBIB = args.out_pbib
    OUT_AUTHERS = args.out_authers
    adminbib = AdminBibText(BIBPATH)
    if OUT_DOI:
        adminbib.to_dois(OFILE, PIDS)
    elif OUT_PBIB:
        adminbib.to_bib(OFILE, PIDS)
    elif OUT_AUTHERS:
        adminbib.to_authers(OFILE, PIDS)
    else:
        raise AssertionError("")
