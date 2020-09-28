from string import Template
from Helper import *


class PromotedItem:
    def __init__(self, name, prices, url, rating = 0):
        self.name = name
        self.prices = prices
        self.url = url
        self.rating = 0

    def __getPrice(self):
        return ' - '.join(map(str, self.prices))

    def info(self):
        return trim_indent(Template("""
        Name: $name
        Price: $price
        Url: $url
        Rating: $rating
    """).safe_substitute(name=self.name, price=self.__getPrice(), url=self.url, rating=self.rating))
