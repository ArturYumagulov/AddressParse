import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class Browser:
    def __init__(self):
        self.driver: webdriver = webdriver.Chrome()
        self.urls_list = []

    def search_2gis_form(self, text: str) -> None:
        """Передача данных в поле поиска и нажатие кнопки ENTER"""

        search_form = self.driver.find_element(By.XPATH, '//input[@enterkeyhint="search"]')

        search_form.send_keys(text)
        time.sleep(1)
        search_form.send_keys(Keys.ENTER)

    def get_point_data(self, url) -> None:

        self.driver.get(url.get_attribute('href'))
        print(self.driver.find_element(By.CLASS_NAME, '_tvxwjf').text)
        print(self.driver.find_element(By.CLASS_NAME, '_oqoid').text)
        print(self.driver.find_element(By.CLASS_NAME, '_1p8iqzw').text)
        phone_block = self.driver.find_element(By.CLASS_NAME, '_b0ke8')
        phone_block.find_element(By.TAG_NAME, 'button').click()
        time.sleep(2)
        phone = self.driver.find_element(By.TAG_NAME, 'bdo').text
        print(phone)
        email = self.driver.find_element(By.CSS_SELECTOR, 'div._599hh > div:nth-child(4)').text
        print(email)

    def double_gis_parse_url(self, url: str, location: str):
        """Парсинг 2GIS"""

        self.driver.get(url)
        self.driver.implicitly_wait(10)
        # self.driver.maximize_window()

        # close footer
        footer = self.driver.find_element(By.TAG_NAME, 'footer')
        footer.find_element(By.TAG_NAME, 'svg').click()

        # search data
        self.search_2gis_form(location)
        time.sleep(1)
        self.search_2gis_form(search)

        # close filter
        filters = self.driver.find_element(By.XPATH, "//button/span[contains(text(),'Фильтры')]")
        filters.click()
        time.sleep(1)

        # click paginator

        paginator = self.driver.find_element(
            By.XPATH,
            '//*[@id="root"]/div/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/div/'
            'div/div/div[3]')
        pages = paginator.find_elements(By.TAG_NAME, 'a')
        for page in pages:
            page.click()
            time.sleep(2)

        # urls = self.driver.find_elements(By.CSS_SELECTOR, 'div._zjunba > a')
        # print(len(urls))
        #
        # # parse urls
        # for url in urls:
        #     url = url.get_attribute('href')
        #     self.urls_list.append(url)
        #
        # print(len(self.urls_list))


if __name__ == '__main__':
    browser = Browser()
    gis_2 = "https://2gis.ru/"
    city = "Набережные Челны"
    search = "Автосервис"
    browser.double_gis_parse_url(gis_2, location=city)
    time.sleep(5)
    browser.driver.close()
