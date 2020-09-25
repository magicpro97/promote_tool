from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from Helper import scroll_down
from abc import ABC, abstractmethod


class LazyPageThread(ABC):
    def __init__(self, keywords, url):
        self.keywords = keywords
        self.url = url
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.html = ""

    def __cleanKeywords(self):
        print('Cleaning keyword...')
        for key in self.keywords:
            key = key.strip()

        print('Keywords cleaned...')
        print("KEYWORD:::" + str(self.keywords))

    def run(self, keyClass, classForScroll):
        self.__cleanKeywords()

        print('Make request to: ' + self.url)
        self.driver.get(self.url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, keyClass))
            )
            scroll_down(
                self.driver, "document.getElementsByClassName('" + classForScroll + "')[0].clientHeight")
        finally:
            self.html = self.driver.page_source
            self.driver.quit()

        self.handleResult()

    @abstractmethod
    def handleResult(self):
        pass
