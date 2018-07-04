#!/usr/bin/env python3

import argparse
import glob
import os
import subprocess

ENV = os.environ
CWD = os.getcwd()
TMP_SETUP = os.path.join(CWD, "setup.py")

if __name__ == "__main__":
    selfexist_path = os.path.split(__file__)[0]
    setupf_path = os.path.join(selfexist_path, "DB/setup.py")
    main_message = "this program is helpful for making setup.py for "\
                   "cython_program"
    parser = argparse.ArgumentParser(description=main_message)
    parser.add_argument("cython_f", type=str, nargs="*")
    parser.add_argument("--all", default=False, const=True,
                        action="store_const")
    args = parser.parse_args()
    file_li = glob.glob("*")
    if args.all:
        pyx_file_li = [f_name for f_name in file_li 
                       if ".pyx" in f_name]
    else:
        pyx_file_li = args.cython_f
    print(pyx_file_li)
    for pyxf in pyx_file_li:
        tmp_setup = open(TMP_SETUP, "w")
        proc1 = subprocess.Popen(["sed",
                                  's/' + '_'*15 + '/' + pyxf + '/g',
                                  setupf_path], stdout = tmp_setup)
        proc1.communicate()
        tmp_setup.close()
        proc2 = subprocess.Popen(["python3", "setup.py", "build_ext", "-i"])
        proc2.communicate()
