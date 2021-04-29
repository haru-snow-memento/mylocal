#!/usr/bin/env python3


import argparse
from argparse import RawTextHelpFormatter
import os
import shutil
from subprocess import run
import subprocess
from more_itertools import consume
OPEN_CMD = "open"
OPEN_CMD_BASE = "open {}"


def fnmstr(path_str):
    if not os.path.exists(path_str):
        mes = "{} is not file.".format(
                                    path_str
                                      )
        raise OSError(mes)
    return path_str


def open_file(fpath):
    shutil.which(OPEN_CMD) is not None
    abs_path = os.path.abspath(fpath)
    cmd = OPEN_CMD_BASE.format(abs_path)
    _ = run(cmd, env=os.environ.copy(),
            shell=True)


class FileRenamer(object):
    def __init__(self, fpaths):
        self._fpath = [os.path.abspath(fpath)
                       for fpath in fpaths]

    def _coroutine_rename_files(self):
        for fpath in self._fpath:
            dpath, base_name = os.path.split(
                                         fpath)
            mes = "will convert {} into what?".format(
                                                base_name)
            yield
            new_fnm = input(mes)
            new_path = os.path.join(dpath,
                                    new_fnm)
            os.rename(fpath, new_path)
            mes = "have converted {} into {}".format(
                                                base_name, new_fnm)
            print(mes)

    def start_file(self, fpath):
        open_file(fpath)

    def coroutine_interactive_rename(self, visualize=True):
        rename_iter = self._coroutine_rename_files()
        for fpath in self._fpath:
            next(rename_iter)
            import ipdb; ipdb.set_trace()
            if visualize:
                self.start_file(fpath)
            yield
        try:
            next(rename_iter)
        except StopIteration:
            yield

    def run(self, visualize=True):
        tmp_iter = self.coroutine_interactive_rename(
                                            visualize=True)
        consume(tmp_iter)


if __name__ == "__main__":
    msg = "this program rename files simultaniously and interactively."
    parser = argparse.ArgumentParser(
                            description=msg,
                            fromfile_prefix_chars="@",
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument("files", type=fnmstr, nargs="*")
    parser.add_argument("--off_visualize", action="store_false",
                        default=True)
    args = parser.parse_args()
    FILES = args.files
    OFF_VISUALIZE = args.off_visualize
    file_renamer = FileRenamer(FILES)
    file_renamer.run(OFF_VISUALIZE)
