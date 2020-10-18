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


def load_bib_to_bibDB(bibpath):
    bibpath = fnmstr(bibpath)
    with open(bibpath, "r") as read:
        strings = read.read()
    bibDB = bparser.parse(strings)
    return bibDB


def load_entries_from_bib(bibpath):
    bibpath = fnmstr(bibpath)
    with open(bibpath, "r") as read:
        strings = read.read()
    bibDB = bparser.parse(strings)
    entries = bibDB.get_entry_list()
    return entries


def write_bibDB_to_bib(bibDB, wpath):
    if not isinstance(bibDB, BibDatabase):
        raise AssertionError(
                "bibDB must be BibDatabase's instance.")
    bibwriter = BibTexWriter()
    text = bibwriter.write(bibDB)
    with open(wpath, 'w') as write:
        write.write(text)


class AdminBibText(object):
    def __init__(self, bib_paths):
        self.tot_entries = []
        for bib_path in bib_paths:
            self._add_entries_from_bibpath(bib_path)

    def _add_entries_from_bibpath(self, bibpath):
        tmp_entries = load_entries_from_bib(bibpath)
        self.tot_entries.extend(tmp_entries)

    def _gene_key_values(self, key):
        for num, entry_dict in enumerate(self.tot_entries):
            if key not in entry_dict:
                mes = "{} : unknown key {}".format(num, key)
                print(mes)
            else:
                value = entry_dict[key]
                yield value

    def write_key_values(self, key, wpath, pids=None, mode="w"):
        with open(wpath, mode) as write:
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

    def write_dois(self, wpath, pids=None, mode="w"):
        self.write_key_values(DOI_KEY, wpath,
                              pids=pids, mode=mode)

    def write_pages(self, wpath, pids=None, mode="w"):
        self.write_key_values(
                        PAGES_KEY, wpath,
                        pids=pids, mode=mode)

    def write_volumes(self, wpath, pids=None, mode="w"):
        self.write_key_values(VOLUME_KEY,
                              wpath, pids=pids,
                              mode=mode)

    def write_journals(self, wpath, pids=None, mode="w"):
        self.write_key_values(
                        JOURNAL_KEY, wpath,
                        pids=pids, mode=mode)

    def write_authers(self, wpath, pids=None, mode="w"):
        self.write_key_values(
                        AUTHER_KEY, wpath,
                        pids=pids, mode=mode)

    def write_abstructs(self, wpath,
                        pids=None, mode="w"):
        self.write_key_values(
                        ABST_KEY, wpath,
                        pids=pids, mode=mode)

    def make_bibtexts(self, pids=None):
        new_bibdata = BibDatabase()
        entries_list = []
        if pids is None:
            entries_list = copy.deepcopy(self.tot_entries)
        else:
            for num, entry_dict in enumerate(self.tot_entries):
                if num in pids:
                    entries_list.append(entry_dict)
        new_bibdata.entries = entries_list
        return new_bibdata

    def write_bib(self, wpath, pids=None):
        new_bibdata = self.make_bibtexts(pids=pids)
        write_bibDB_to_bib(new_bibdata, wpath)
