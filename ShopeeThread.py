from Helper import *
from LazyPageThread import LazyPageThread
from bs4 import BeautifulSoup
from PromotedItem import PromotedItem


class ShopeeThread(LazyPageThread):
    def __init__(self, keywords, url):
        super(ShopeeThread, self).__init__(keywords, url)

    def run(self):
        super(ShopeeThread, self).run(keyClass="shopee-search-item-result__items",
                                      classForScroll="row shopee-search-item-result__items",
                                      classForPageNumber="shopee-mini-page-controller__total",
                                      )

    def handle_result(self):
        print('------------------------------')

        bsoup = BeautifulSoup(self.html, 'lxml')

        items = bsoup.find_all(
            "div", {"class": "col-xs-2-4 shopee-search-item-result__item", })

        self.item_num = len(items)

        print("TOTAL:::" + str(self.item_num))

        products = []

        for item in items:
            sold_item = item.find('div', {'class': '_18SLBt'})

            stars = item.find_all('div', {'class': 'shopee-rating-stars__lit'})

            rating = .0
            if stars is not None:
                for star in stars:
                    rating = rating + \
                        float(str(star.get('style'))[7:-2]) / 100.0

            product = PromotedItem(name=item.find("div", {"class": "_1NoI8_"}).string,
                                   prices=list(map(lambda item: int(item.string.replace(
                                       '.', '')), item.select("span._341bF0"))),
                                   url=item.a.get("href"),
                                   sold=self.getSoldNum(
                                       sold_item.string) if sold_item is not None and sold_item.string is not None else 0,
                                   rating=rating,
                                   )
            products.append(product)

        return products

    def getSoldNum(self, value):
        return value_to_num(value.replace('Đã bán ', ''))

    def sort(self, value):
        return value.prices[0]
