#!/usr/bin/env python3


# formal lib
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.encoders import encode_base64
import mimetypes
from mimetypes import guess_type
import os
from collections import Sequence
from itertools import zip_longest
import copy


class AdminGmail(object):
    host = "smtp.gmail.com"
    port = 587

    def __init__(self, login_maddr, login_pass):
        self.login_maddr = login_maddr
        self.login_pass = login_pass
        self.attachment_mimeli = []

    def set_txtmessage(self, from_addr, to_addr,
                       cc="", bcc="", subject="", body=""):
        # MIMEText is a derived dict type.
        self.from_addr = from_addr
        self.to_addr = to_addr
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Bcc"] = bcc
        msg["Date"] = formatdate()
        self.msg = msg

    def set_origcont_with_path_myme(self,
                                    cont_fpath_myme_ins):
        # 1
        if type(cont_fpath_myme_ins) != ContFpathMimetype:
            raise TypeError("you enter invalid type "
                            "to attachdict.")
        self.cont_fpath_myme_ins = cont_fpath_myme_ins

    def set_attachment_mimes_li(self):
        # 4
        if not hasattr(self, "cont_fpath_myme_ins"):
            raise AttributeError("in advence, you must use "
                                 "set_origcont_with_path_myme")
        for fpath, mimetype in self.cont_fpath_myme_ins:
            self.add_attachment_mime(fpath, mimetype)

    def add_attachment_mime(self, fpath, assign_mime):
        # it's called by set_attachment_mimes_li
        assign_mime = guess_mimetype(fpath)
        attach_mime = MIMEBase(assign_mime["type"],
                               assign_mime["subtype"])
        base_fnm = os.path.basename(fpath)
        with open(fpath, "rb") as read:
            attach_mime.set_payload(read.read())
        encode_base64(attach_mime)
        attach_mime.add_header("Content-Disposition", "attachment",
                               filename=base_fnm)
        self.attachment_mimeli.append(attach_mime)

    def set_msg_with_attachment(self, from_addr, to_addr,
                                cc="", bcc="",
                                subject="", body=""):
        """
        MIMEMultipart can have multiple MIMEs.
        """
        self.from_addr = from_addr
        self.to_addr = to_addr
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Date"] = formatdate()
        body_mime = MIMEText(body)
        msg.attach(body_mime)
        if len(self.attachment_mimeli) == 0:
            print("attachment li is empty.")
        for mime in self.attachment_mimeli:
            msg.attach(mime)
        self.msg = msg

    def simply_set_msg_with_attachment(self, from_addr, to_addr, fpath,
                                       cc="", bcc="", subject="",
                                       body=""):
        self.from_addr = from_addr
        self.to_addr = to_addr
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = to_addr
        msg["Date"] = formatdate()
        body_mime = MIMEText(body)
        msg.attach(body_mime)
        attach_mime = self.convert_file_to_mime(fpath)
        msg.attach(attach_mime)
        self.msg = msg

    def convert_file_to_mime(self, fpath):
        assign_mime = guess_mimetype(fpath)
        attach_mime = MIMEBase(assign_mime["type"],
                               assign_mime["subtype"])
        base_fnm = os.path.basename(fpath)
        with open(fpath, "rb") as read:
            attach_mime.set_payload(read.read())
        encode_base64(attach_mime)
        attach_mime.add_header("Content-Disposition", "attachment",
                               filename=base_fnm)
        return attach_mime

    def send(self):
        with smtplib.SMTP(self.host, self.port) as smtpobj:
            # confirm server
            smtpobj.ehlo()
            # the following section is encrypted.
            smtpobj.starttls()
            smtpobj.ehlo()
            smtpobj.login(self.login_maddr, self.login_pass)
            smtpobj.sendmail(self.from_addr,
                             self.to_addr,
                             self.msg.as_string())
        print("email is completely sent.")


def guess_mimetype(fpath):
    ktpl = ["type", "subtype"]
    total_mtype = mimetypes.guess_type(fpath)[0]
    main_type, subtype = total_mtype.split("/")
    vatp = (main_type, subtype)
    mimetype = dict(zip(ktpl, vatp))
    return mimetype


"""
def guess_mimetype(fpath):
    ktpl = ["type", "subtype"]
    vatp = mimetypes.guess_type(fpath)
    mimetype = dict(zip(ktpl, vatp))
    return mimetype
"""


class ContFpathMimetype(Sequence):
    def __init__(self, fpaths, mimetypes=[]):
        self.fpaths = fpaths
        self.mimetypes = mimetypes
        self.unknown_mimetype = {"type": None,
                                 "subtype": None}
        self.reset_path_mime_pair_li()

    def reset_path_mime_pair_li(self):
        self.path_mimetype_pair_li = []
        for path, mimetype in zip_longest(self.fpaths,
                                          self.mimetypes):
            if not os.path.exists(path):
                continue
            if mimetype is None:
                none_mimedict = copy.deepcopy(
                                    self.unknown_mimetype
                                             )
                mimetype = guess_mimetype(path)
            self.path_mimetype_pair_li.append((path, mimetype))

    def __len__(self):
        return len(self.path_mimetype_pair_li)

    def __getitem__(self, key):
        return self.path_mimetype_pair_li[key]

    def __setitem__(self, key, va):
        if type(va) == tuple:
            raise AttributeError("you must enter tuple object")
        path, mime = va
        if not os.path.exists(path):
            raise OSError(path + " is not existing")
        if mime is None:
            mime = guess_mimetype(path)
        self.path_mimetype_pair_li[key] = va

    def __iter__(self):
        for otple in self.path_mimetype_pair_li:
            yield otple
