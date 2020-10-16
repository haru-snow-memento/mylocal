#!/usr/bin/env python3

# formal lib
import os
import copy
#
import rispy
from RISparser.config import TAG_KEY_MAPPING
from RISparser import readris
from abc import ABCMeta, abstractmethod
RIS_VALS = list(TAG_KEY_MAPPING.values())


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


def load_entries_from_ris(ris_fpath):
    ris_fpath = fnmstr(ris_fpath)
    with open(ris_fpath, "r") as read:
        entries = readris(read)
    return entries


def write_entries_to_ris(bibDB, wpath):
    if not isinstance(bibDB, BibDatabase):
        raise AssertionError(
                "bibDB must be BibDatabase's instance.")
    bibwriter = BibTexWriter()
    text = bibwriter.write(bibDB)
    with open(wpath, 'w') as write:
        write.write(text)


class AdminRISText(object, metaclass=ABCMeta):
    def __init__(self, ris_texts):
        self.ris_texts = ris_texts

    def _gene_entries_from_ristxts(self, ris_texts):
        for ris_text in ris_texts:
            with oe

    def load_entries_from_ris(self):
        pass

    def _gene_key_values(self, key):
        for num, bib_dict in enumerate(self._bib_dicts):
            if key not in bib_dict:
                mes = "{} : unknown key {}".format(num, key)
                print(mes)
            else:
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
