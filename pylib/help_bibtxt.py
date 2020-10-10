#!/usr/bin/env python3

# formal lib
import os
import copy
from bibtexparser import bparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
# my lib

DOI_KEY = "doi"
PAGES_KEY = "pages"
VOLUME_KEY = "volume"
JOURNAL_KEY = "jounal"
AUTHER_KEY = "auther"
ABST_KEY = "abstract"
URL_KEY = "url"
YEAR_KEY = "year"
TITLE_KEY = "title"
ENTRYTYPE_KEY = "ENTRYTYPE"
ID_KEY = "ID"
BIB_KEYS = [DOI_KEY, PAGES_KEY,
            VOLUME_KEY, JOURNAL_KEY, AUTHER_KEY,
            ABST_KEY, URL_KEY, YEAR_KEY, TITLE_KEY,
            ENTRYTYPE_KEY, ID_KEY]


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


def load_bib_to_bibDB(bib_txt):
    fnmstr
    with open(bib_txt, "r") as read:
        strings = read.read()
    bibDB = bparser.parse(strings)
    return bibDB


def write_bibDB_to_bib(bibDB, wpath):
    if not isinstance(bibDB, BibDatabase):
        raise AssertionError(
                "bibDB must be BibDatabase's instance.")
    bibwriter = BibTexWriter()
    text = bibwriter.write(bibDB)
    with open(wpath, 'w') as write:
        write.write(text)


class AdminBibText(object):
    def __init__(self, bib_path):
        self._BibDB = load_bib_to_bibDB(bib_path)
        self._entries_dict = self._BibDB.entries_dict
        self._keys = list(
                        self._entries_dict.keys())
        self._bib_dicts = list(
                            self._BibDB.get_entry_list())

    def _gene_key_values(self, key):
        for bib_dict in self._bib_dicts:
            value = bib_dict[key]
            yield value

    def to_key_values(self, key, wpath, pids=None):
        with open(wpath, "w") as write:
            for num, value in enumerate(
                                self._gene_key_values(key)):
                if pids is None:
                    line = "{}\n".format(value)
                    write.write(line)
                elif num in pids:
                    line = "{}\n".format(value)
                    write.write(line)
                else:
                    pass

    def to_dois(self, wpath, pids=None):
        self.to_key_values(DOI_KEY, wpath,
                           pids=pids)

    def to_pages(self, wpath, pids=None):
        self.to_key_values(PAGES_KEY, wpath,
                           pids=pids)

    def to_volumes(self, wpath, pids=None):
        self.to_key_values(VOLUME_KEY,
                           wpath, pids=pids)

    def to_journals(self, wpath, pids=None):
        self.to_key_values(
                    JOURNAL_KEY, wpath,
                    pids=pids)

    def to_authers(self, wpath, pids=None):
        self.to_key_values(AUTHER_KEY, wpath,
                           pids=pids)

    def to_abstructs(self, wpath,
                     pids=None):
        self.to_key_values(ABST_KEY, wpath,
                           pids=pids)

    def make_bibtexts(self, pids=None):
        new_bibdata = BibDatabase()
        entries_list = []
        if pids is None:
            entries_list = copy.deepcopy(self._bib_dicts)
        else:
            for num, entry_dict in enumerate(self._bib_dicts):
                if num in pids:
                    entries_list.append(entry_dict)
        new_bibdata.entries = entries_list
        return new_bibdata

    def to_bib(self, wpath, pids=None):
        new_bibdata = self.make_bibtexts(pids=pids)
        write_bibDB_to_bib(new_bibdata, wpath)
