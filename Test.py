# !/usr/bin/python
# coding=utf-8

from ShopeeThread import ShopeeThread
from Helper import value_to_num
from multiprocessing import freeze_support
import sys

if __name__ == '__main__':
    freeze_support()
    KEYWORDS = "Chuột, Logitech"

    CATEGORY_URL = "https://shopee.vn/search?category=2365"

    sys.setrecursionlimit(25000)
    ShopeeThread(
        keywords=KEYWORDS,
        url=CATEGORY_URL,
    ).run()
