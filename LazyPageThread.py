from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Helper import scroll_down
from abc import ABC, abstractmethod
import psutil
from multiprocessing import Pool


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

        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920x1080")
        self.options.add_argument("start-maximised")

    def run(self, keyClass, classForScroll, classForPageNumber):
        cpu_num = psutil.cpu_count()
        print("Processor:::" + str(cpu_num))
        pool = Pool(cpu_num)

        page = self.page_range[0]
        last_page = self.page_range[1]

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("start-maximised")

        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=self.options)
        driver.get(self.url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, classForPageNumber))
            )
        finally:
            self.total_page = int(
                driver.find_element_by_class_name(classForPageNumber).text)
            driver.quit()

        # for i in range(self.total_page):
        #     pool.apply_async(self.__crawling, (self.url, i,))

        results = [pool.apply_async(self.crawling, (self.url, keyClass,
                                                    classForScroll, i, self.options)) for i in range(self.total_page)]
        print([res.get(timeout=30) for res in results])

        # while self.has_next_page():
        #     self.url = self.url + "&page=" + str(page)
        #     print('Make request to: ' + self.url)

        #     driver = webdriver.Chrome(
        #         ChromeDriverManager().install(), chrome_options=options)
        #     driver.get(self.url)

        #     try:
        #         WebDriverWait(driver, 10).until(
        #             EC.presence_of_element_located(
        #                 (By.CLASS_NAME, keyClass))
        #         )
        #         scroll_down(
        #             driver, "document.getElementsByClassName('" + classForScroll + "')[0].clientHeight")
        #     finally:
        #         self.html = driver.page_source
        #         driver.quit()

        #     self.handle_result()

        #     if last_page > -1:
        #         if page <= last_page and self.has_next_page():
        #             page = page + 1
        #     elif self.has_next_page():
        #         page = page + 1

    def crawling(self, url, keyClass, classForScroll, page_num, options):
        url = url + "&page=" + str(page_num)
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        driver.get(url)

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
        
        return "PAGE:::"+ url + " DONE!"

    @abstractmethod
    def handle_result(self):
        pass

    def has_next_page(self):
        return self.item_num == self.max_item

    @abstractmethod
    def get_total_page_num(self):
        pass
