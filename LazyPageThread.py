from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Helper import scroll_down
from abc import ABC, abstractmethod
from multiprocessing import Pool, Manager, Process
import psutil


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

        products = Manager().list()

        results = [pool.apply_async(self.crawling, (
            self.url,
            keyClass,
            classForScroll,
            i,
            self.options,
            products,
        ),
        ) for i in range(self.total_page)]

        for res in results:
            res.wait(timeout=60)
            
        print(len(products))

    @abstractmethod
    def sort(self, value):
        pass

    def crawling(self, url, keyClass, classForScroll, page_num, options, products):
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

        products.extend(self.handle_result())

    @abstractmethod
    def handle_result(self):
        pass
