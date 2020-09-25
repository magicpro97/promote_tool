# !/usr/bin/python
# coding=utf-8

from bs4 import BeautifulSoup
# import requests
from Helper import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from PromotedItem import PromotedItem
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# caps = DesiredCapabilities.FIREFOX.copy()
# caps['marionette'] = False
# driver = webdriver.Firefox(capabilities=caps)


KEYWORDS = "Chuột, Logitech, Bluetooth".split(',')

clear()
print('-----BEGIN-----')

print('Cleaning keyword...')
for key in KEYWORDS:
    key = key.strip()

print('Keywords cleaned...')
print("KEYWORD:::" + str(KEYWORDS))

print('Make request to: ')
# res = requests.get('https://shopee.vn/search?category=2365&keyword=chu%E1%BB%99t%20logitech')

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(
    'https://shopee.vn/search?category=2365&keyword=chu%E1%BB%99t%20logitech')

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "shopee-search-item-result__items"))
    )
    scroll_down(
        driver, "document.getElementsByClassName('row shopee-search-item-result__items')[0].clientHeight")
finally:
    html = driver.page_source
    driver.quit()

print('------------------------------')

# bsoup = BeautifulSoup(res.text, 'lxml')
bsoup = BeautifulSoup(html, 'lxml')

items = bsoup.findAll(
    "div", {"class": "col-xs-2-4 shopee-search-item-result__item", })

print("TOTAL:::" + str(len(items)))

for item in items:
    #temp = item.find('div', {'class': '_3eufr2'})
    product = PromotedItem(name=item.find("div", {"class": "_1NoI8_"}).string,
                           prices=list(map(lambda item: int(item.string.replace(
                               '.', '')), item.select("span._341bF0"))),
                           url=item.a.get("href"),
                           )
    print(product.info())

print('-----END-----')
