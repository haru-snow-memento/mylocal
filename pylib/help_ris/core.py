#!/usr/bin/env python3

# formal lib
import os
#
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
import rispy
from RISparser.config import TAG_KEY_MAPPING
from RISparser import readris
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


def write_entries_to_ris(entries, wpath):
    if not isinstance(entries, list):
        raise AssertionError(
                "entries must be dictionary.")
    with open(wpath, 'w') as write:
        rispy.dump(entries, write)


class AdminRISText(object):
    def __init__(self, ris_texts):
        self.ris_texts = ris_texts
        tmp_iter = self._gene_entry_from_ristxts()
        self.entries = list(tmp_iter)

    def _gene_entry_from_ristxts(self):
        for ris in self.ris_texts:
            ris = fnmstr(ris)
            entries = load_entries_from_ris(ris)
            for entry in entries:
                yield entry

    def _set_entries_from_ris(self):
        tmp_iter = self._gene_entry_from_ristxts()
        self.entries = list(tmp_iter)

    def _gene_key_values(self, key):
        for num, entry in enumerate(self.entries):
            if key not in entry:
                mes = "{} : unknown key {}".format(num, key)
                print(mes)
            else:
                value = entry[key]
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

    def to_bib(self, wpath, pids=None):
        entries = []
        for num, entry in enumerate(self.entries):
            if pids is None:
                entries.append(entry)
            elif num in pids:
                entries.append(entry)
            else:
                raise AssertionError("")
        bibdb = BibDatabase()
        bibdb.entries = entries
        with open(wpath, "w") as write:
            bibtexparser.dump(bibdb, write)

    def to_ris(self, wpath, pids=None):
        entries = []
        for num, entry in enumerate(self.entries):
            if pids is None:
                entries.appned(entry)
            elif num in pids:
                entries.append(entry)
            else:
                raise AssertionError("")
        write_entries_to_ris(entries, wpath)