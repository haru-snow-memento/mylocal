#!/usr/bin/env python3


# formal lib
import argparse
import glob
import re
import os
# mylib
from gmail import AdminGmail
from gmail import ContFpathMimetype


def print_global_varibales():
    glva_dict = globals()
    print_dict = {key: va for key, va in glva_dict.items()
                  if key.isupper()}
    print("== global varibale is in the following. ==")
    print(print_dict)
    print("==========================================")


def walk_for_match_file(root, re_pat):
    pat_ins = re.compile(re_pat)
    for main_dpath, sub_dpath, files in os.walk(root):
        fnms = (fnm for fnm in files
                if pat_ins.search(fnm) is not None)
        for fnm in fnms:
            fpath = os.path.join(main_dpath, fnm)
            yield fpath


def make_arg_parser():
    msg = "it send email with a pdf to a kindle account."
    parser = argparse.ArgumentParser(description=msg,
                                     fromfile_prefix_chars="@")
    # necessary argument
    parser.add_argument("pdf_paths", type=str, nargs="*")
    parser.add_argument("--gmail_passwd", type=str,
                        nargs="?", required=True)
    parser.add_argument("--gmail_account", type=str,
                        nargs="?", required=True)
    parser.add_argument("--to_address", type=str,
                        nargs="?", required=True)
    # optional argument
    # # glob and walk
    effepaths_gp = parser.add_argument_group("effectively_get_paths")
    effepaths_gp.add_argument("--glob_style", nargs="?",
                              default=None, type=str)
    effepaths_gp.add_argument("--walk_pat", nargs="?",
                              default=None, type=str)
    effepaths_gp.add_argument("--root", nargs="?", default=None, type=str)
    parser.add_argument("--bcc", nargs="?", type=str, default="")
    parser.add_argument("--cc", nargs="?", type=str, default="")
    parser.add_argument("--body", nargs="?", type=str, default="")
    parser.add_argument("--subject", nargs="?", type=str,
                        default="")
    # especial operation argument
    hmsg = "it needs MIME_DICT using extension and get MIME type."
    parser.add_argument("--assign_mime", nargs="*",
                        type=str, default=None, help=hmsg)
    return parser
    

if __name__ == "__main__":
    parser = make_arg_parser()
    args = parser.parse_args()
    # necessay arguments
    PDF_PATHS = args.pdf_paths
    GMAIL_PASSWD = args.gmail_passwd
    GMAIL_ACCOUNT = args.gmail_account
    TO_ADDRESS = args.to_address
    # optinal argument
    BCC = args.bcc
    CC = args.cc
    BODY = args.body
    SUBJECT = args.subject
    GLOB_STYLE = args.glob_style
    WALK_PAT = args.walk_pat
    ROOT = args.root
    if GLOB_STYLE is not None:
        PDF_PATHS = glob.glob(GLOB_STYLE)
    elif WALK_PAT is not None:
        if ROOT is None:
            raise AssertionError("you must set ROOT argument")
        PDF_PATHS = list(walk_for_match_file(ROOT, WALK_PAT))
    print_global_varibales()
    # === main part ==
    admin_gmail_ins = AdminGmail(GMAIL_ACCOUNT, GMAIL_PASSWD)
    cont_fpath_mimtype = ContFpathMimetype(PDF_PATHS)
    admin_gmail_ins.set_origcont_with_path_myme(
                                    cont_fpath_mimtype)
    admin_gmail_ins.set_attachment_mimes_li()
    admin_gmail_ins.set_msg_with_attachment(
                                         GMAIL_ACCOUNT,
                                         TO_ADDRESS,
                                         CC, BCC,
                                         SUBJECT, BODY)
    admin_gmail_ins.send()
