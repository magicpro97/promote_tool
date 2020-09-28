# !/usr/bin/python
# coding=utf-8

from ShopeeThread import ShopeeThread


if __name__ == '__main__':
    KEYWORDS = "Chuột, Logitech"

    CATEGORY_URL = "https://shopee.vn/search?category=2365"

    ShopeeThread(keywords=KEYWORDS,
                 url=CATEGORY_URL).run()
