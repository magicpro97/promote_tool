# !/usr/bin/python
# coding=utf-8

from ShopeeThread import ShopeeThread
from Helper import value_to_num
import sys


KEYWORDS = "Chuột, Logitech"

CATEGORY_URL = "https://shopee.vn/search?category=2365"

sys.setrecursionlimit(25000)

if __name__ == '__main__':

    ShopeeThread(
        keywords=KEYWORDS,
        url=CATEGORY_URL,
    ).run()
