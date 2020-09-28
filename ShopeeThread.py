from Helper import *
from LazyPageThread import LazyPageThread
from bs4 import BeautifulSoup
from PromotedItem import PromotedItem


class ShopeeThread(LazyPageThread):
    def __init__(self, keywords, url):
        super(ShopeeThread, self).__init__(keywords, url)
        self.max_item = 50
        self.item_num = self.max_item

    def run(self):
        super(ShopeeThread, self).run(keyClass="shopee-search-item-result__items",
                                      classForScroll="row shopee-search-item-result__items",
                                      classForPageNumber="shopee-mini-page-controller__total",
                                      )

    def handle_result(self):
        print('------------------------------')

        bsoup = BeautifulSoup(self.html, 'lxml')

        items = bsoup.findAll(
            "div", {"class": "col-xs-2-4 shopee-search-item-result__item", })

        self.item_num = len(items)

        print("TOTAL:::" + str(self.item_num))

        for item in items:
            product = PromotedItem(name=item.find("div", {"class": "_1NoI8_"}).string,
                                   prices=list(map(lambda item: int(item.string.replace(
                                       '.', '')), item.select("span._341bF0"))),
                                   url=item.a.get("href"),
                                   )
            print(product.info())
            
    
    def get_total_page_num(self):
        return super().get_total_page_num()
