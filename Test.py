# !/usr/bin/python
# coding=utf-8

from ShopeeThread import ShopeeThread

KEYWORDS = "Chuột, Logitech"

CATEGORY_URL = "https://shopee.vn/search?category=2365"

SHOPEE = ShopeeThread(keywords=KEYWORDS,
                      url=CATEGORY_URL).run()
