import sys

sys.path.insert(0, "/usr/lib/chromium-browser/chromedriver")  # path to chromedriver
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
service = Service(ChromeDriverManager().install())


class Extract:
    def __init__(self, url, dynamic_content=False):
        self.url = url
        self.dynamic_content = dynamic_content

    def get_urls(self, path_element):
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(self.url)
        previous_height = driver.execute_script("return document.body.scrollHeight")
        links = []
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == previous_height:
                break
            previous_height = new_height

            if self.dynamic_content:
                elements = driver.find_elements(By.CSS_SELECTOR, path_element)
                for element in elements:
                    links.append(element.get_attribute("href"))

        if not self.dynamic_content:
            elements = driver.find_elements(By.CSS_SELECTOR, path_element)
            for element in elements:
                links.append(element.get_attribute("href"))

        driver.quit()
        return links

    def get_data(self):

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(self.url)
        time.sleep(5)
        content = driver.page_source
        driver.quit()
        return content
