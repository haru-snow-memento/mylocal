#!/usr/bin/env python3


# formal lib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from abc import ABCMeta, abstractmethod
from inputimeout import inputimeout, TimeoutOccurred
import re
# my lib
URL = "https://site0.sbisec.co.jp/marble/market/calendar/schedule/foreign.do?Param6=US"


class AccessBase(object, metaclass=ABCMeta):
    def __init__(self, options_ins=None,
                 size=(1440, 783), implicit_wait=3):
        cond1 = options_ins is None
        cond2 = isinstance(options_ins, Options)
        if not (cond1 or cond2):
            raise TypeError("Use Options in selenium libraries.")
        self.driver = webdriver.Chrome(options=options_ins)
        self._set_windows_size(size)
        self._set_implicit_wtime(implicit_wait)

    def _set_windows_size(self, size=(1440, 783)):
        self.size = size

    def _set_implicit_wtime(self, implicit_time=5):
        self.implicit_time = implicit_time

    def _initial_access(self):
        self.driver.set_window_size(*self.size)
        self.driver.implicitly_wait(self.implicit_time)

    @classmethod
    @abstractmethod
    def access(self):
        raise NotImplementedError("")

    def wait(self, time=300):
        time.sleep(time)

    def quit(self):
        self.driver.quit()

    def input_wait(self, wtime=300):
        try:
            _ = inputimeout(
                        "waiting for {}:".format(wtime),
                        timeout=wtime)
        except TimeoutOccurred:
            pass
        self.quit()

    def set_reins_source(self, url_re):
        re_ins = re.compile(url_re)
        cur_url = self.driver.current_url
        self.re_ins = re_ins

    def check_source(self):
        re_object = self.re_ins.match(
                            self.driver.current_url)
        if re_object is not None:
            return True
        else:
            return False


class ExtracterCallConference(object):
    def __init__(self):
        pass
