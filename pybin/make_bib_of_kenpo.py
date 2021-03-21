#!/usr/bin/env python3

# formal lib
from bibtexparser import bparser
import argparse
from argparse import RawTextHelpFormatter
import os
# my lib
from help_bib import write_bibDB_to_bib
# my lib
BASE_BIBTXT = """
@article{kenpo,
  title = {None},
  author = {None},
  journal = {研(CTI)研究報告},
  volume = {10953},
  year = {2020},
  month = {Apr},
  issue = {None},
  pages = {None},
  numpages = {None},
  publisher = {研(CTI)},
  doi = {None},
  url = {None}
}
"""
BIBDATA = bparser.parse(BASE_BIBTXT)
URL_KEY = 'url'
DOI_KEY = 'doi'
PUBLISHER_KEY = 'publisher'
MONTH_KEY = 'month'
YEAR_KEY = 'year'
VOLUME_KEY = 'volume'
JOURNAL_KEY = 'journal'
AUTHER_KEY = 'author'
TITLE_KEY = 'title'
ISSUE_KEY = "issue"
PAGES_KEY = "pages"
NUMPAGES_KEY = "numpages"
ENTRYTYPE_KEY = 'ENTRYTYPE'
ID_KEY = 'ID'


class AutherNameStr():
    def __init__(self, name_sep=", ", hum_sep="and"):
        self.name_sep = name_sep
        self.hum_sep = hum_sep

    def __call__(self, hum_name):
        if self.name_sep not in hum_name:
            emes = "invalid name separation signal is used."
            raise AssertionError(emes)
        return hum_name

    def convert_names_into_auther(self, names_list):
        assert isinstance(names_list, list)
        auther = self.hum_sep.join(names_list)
        return auther


class WithExt(object):
    def __init__(self, ext):
        self._ext = ext

    def __call__(self, fpath, check_exist=False):
        fnm, ext = os.path.splitext(fpath)
        if self._ext != ext:
            emes = "extension must be {}".format(ext)
            raise OSError(emes)
        if check_exist:
            fpath = os.path.abspath(fpath)
        return fpath


if __name__ == "__main__":
    msg = "this prorgam interactively makes bibdata"
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@",
                                formatter_class=RawTextHelpFormatter)
    parser.add_argument("--out_bib", type=WithExt(".bib"), nargs="?")
    subparsers = parser.add_subparsers(dest="sub_opt")
    make_parser = subparsers.add_parser("make")
    itrctv_parser = subparsers.add_parser("interactive")
    make_parser.add_argument("--title", type=str, nargs="?",
                             required=True)
    make_parser.add_argument("--authers", type=AutherNameStr(), nargs="+",
                             required=True)
    make_parser.add_argument("--journal", type=str, nargs="?",
                             default="研(CTI)研究報告書")
    make_parser.add_argument("--publisher", type=str, nargs="?",
                             default="研究報告書")
    make_parser.add_argument("--volume", type=str, nargs="?",
                             required=True)
    make_parser.add_argument("--year", type=str, nargs="?",
                             required=True)
    make_parser.add_argument("--issue", type=str, nargs="?", default=None)
    make_parser.add_argument("--pages", type=str, nargs="?", default=None)
    make_parser.add_argument("--numpages", type=str, nargs="?", default=None)
    make_parser.add_argument("--month", type=str, nargs="?", default=None)
    make_parser.add_argument("--doi", type=str, nargs="?", default=None)
    make_parser.add_argument("--url", type=str, nargs="?", default=None)
    args = parser.parse_args()
    OUT_BIB = args.out_bib
    SUB_OPT = args.sub_opt
    BIBDATA = bparser.parse(BASE_BIBTXT)
    if SUB_OPT == "make":
        bib_dict = BIBDATA.entries[0]
        TITLE = args.title
        if TITLE is not None:
            bib_dict[TITLE_KEY] = TITLE
        AUTHERS = args.authers
        if AUTHERS is not None:
            auther_str = AutherNameStr().convert_names_into_auther(
                                                            AUTHERS)
            bib_dict[AUTHER_KEY] = auther_str
        JOURNAL = args.journal
        if JOURNAL_KEY is not None:
            bib_dict[JOURNAL_KEY] = JOURNAL
        PUBLISHER = args.publisher
        if PUBLISHER_KEY is not None:
            bib_dict[PUBLISHER_KEY] = PUBLISHER
        VOLUME = args.volume
        if VOLUME is not None:
            bib_dict[VOLUME_KEY] = VOLUME
        YEAR = args.year
        if YEAR_KEY is not None:
            bib_dict[YEAR_KEY] = YEAR
        ISSUE = args.issue
        if ISSUE is not None:
            bib_dict[ISSUE_KEY] = ISSUE
        PAGES = args.pages
        if PAGES is not None:
            bib_dict[PAGES_KEY] = PAGES
        NUMPAGES = args.numpages
        if NUMPAGES is not None:
            bib_dict[NUMPAGES_KEY] = NUMPAGES
        MONTH = args.month
        if MONTH is not None:
            bib_dict[MONTH_KEY] = MONTH
        DOI = args.doi
        if DOI is not None:
            bib_dict[DOI_KEY] = DOI
        URL = args.url
        if URL is not None:
            bib_dict[URL_KEY] = URL
    elif SUB_OPT == "interactive":
        raise AssertionError
    write_bibDB_to_bib(BIBDATA, OUT_BIB)
