# !/usr/bin/python
# coding=utf-8

from ShopeeThread import ShopeeThread

KEYWORDS = "Chuột, Logitech, Bluetooth".split(',')

SHOPEE = ShopeeThread(keywords=KEYWORDS,
                      url="https://shopee.vn/search?category=2365&keyword=chu%E1%BB%99t%20logitech").run()
