#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import argparse
from argparse import RawTextHelpFormatter
import numpy as np

AMAAUC_URL = "https://amaoku.jp"

def gene_price_ratio():
    result = requests.get(AMAAUC_URL)
    source = result.content
    soup = BeautifulSoup(source, "lxml")
    table=soup.findChildren("table")[0]
    for tr_content in table.find_all("tr", class_="category_1"):
        ratio_cont = tr_content.find_all("td")[3].text
        if "%" not in ratio_cont:
            raise TypeError(
                        "invalid contents in table record.")
        ratio = ratio_cont.rstrip("%")
        ratio = float(ratio)
        yield ratio


class RatioChecker(object):
    def __init__(self, price_ratio):
        self.price_ratio = price_ratio

    def __call__(self, ratio_iter):
        if not hasattr(ratio_iter, "__iter__"):
            raise TypeError("not iterable.")
        min_va = np.min(list(ratio_iter))
        self.min_va = min_va
        if min_va < self.price_ratio:
                return True
        return False


if __name__ == "__main__":
    msg = "this program check discount ratio of amazon chickets."
    parser = argparse.ArgumentParser(
                                description=msg,
                                fromfile_prefix_chars="@",
                                formatter_class=RawTextHelpFormatter)
    parser.add_argument("--interval_minute", type=int,
                        nargs="?", default=10)
    parser.add_argument("--price_ratio", type=float,
                        nargs="?", default=81.0)
    args = parser.parse_args()
    INTERVAL_MINUTE = args.interval_minute
    PRICE_RATIO = args.price_ratio
    price_iter = gene_price_ratio()
    ratio_checker = RatioChecker(PRICE_RATIO)
    cond = ratio_checker(price_iter)
    if cond:
        print("Amazon gift price ratio is under {}".format(
                                            self.price_ratio))
    print("minmum value is {}".format(ratio_checker.min_va))
