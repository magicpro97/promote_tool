from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Helper import scroll_down
from abc import ABC, abstractmethod


class LazyPageThread(ABC):
    def __init__(self, keywords, category_url, page_range=[0, -1]):
        print("Cleaning keywords")
        keywords = "%20".join(
            map(lambda item: item.strip(), keywords.split(',')))
        search_url = category_url + "&keyword=" + keywords
        print("Cleaned keywords")

        self.max_item = 0
        self.item_num = 0
        self.page_range = page_range
        self.url = search_url
        self.html = ""

    def run(self, keyClass, classForScroll):
        page = self.page_range[0]
        last_page = self.page_range[1]

        options = Options()
        # options.headless = True

        while self.has_next_page():
            self.url = self.url + "&page=" + str(page)
            print('Make request to: ' + self.url)

            driver = webdriver.Chrome(
                ChromeDriverManager().install(), chrome_options=options)
            driver.get(self.url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, keyClass))
                )
                scroll_down(
                    driver, "document.getElementsByClassName('" + classForScroll + "')[0].clientHeight")
            finally:
                self.html = driver.page_source
                driver.quit()

            self.handle_result()

            if last_page > -1:
                if page <= last_page and self.has_next_page():
                    page = page + 1
            elif self.has_next_page():
                page = page + 1

    @abstractmethod
    def handle_result(self):
        pass

    def has_next_page(self):
        return self.item_num == self.max_item
