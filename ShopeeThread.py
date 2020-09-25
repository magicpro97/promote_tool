from Helper import *
from LazyPageThread import LazyPageThread
from bs4 import BeautifulSoup
from PromotedItem import PromotedItem


class ShopeeThread(LazyPageThread):
    def __init__(self, keywords, url):
        super(ShopeeThread, self).__init__(keywords, url)

    def run(self):
        super(ShopeeThread, self).run(keyClass="shopee-search-item-result__items",
                  classForScroll="row shopee-search-item-result__items")

    def handleResult(self):
        print('------------------------------')

        # bsoup = BeautifulSoup(res.text, 'lxml')
        bsoup = BeautifulSoup(self.html, 'lxml')

        items = bsoup.findAll(
            "div", {"class": "col-xs-2-4 shopee-search-item-result__item", })

        print("TOTAL:::" + str(len(items)))

        for item in items:
            product = PromotedItem(name=item.find("div", {"class": "_1NoI8_"}).string,
                                   prices=list(map(lambda item: int(item.string.replace(
                                       '.', '')), item.select("span._341bF0"))),
                                   url=item.a.get("href"),
                                   )
            print(product.info())
