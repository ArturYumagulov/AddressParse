import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By


class Browser:
    def __init__(self):
        self.driver: webdriver = webdriver.Chrome()
        self.urls_list = []
        self.sleep_time = 2

    def search_2gis_form(self, text: str) -> None:
        """Передача данных в поле поиска и нажатие кнопки ENTER"""

        search_form = self.driver.find_element(By.XPATH, '//input[@enterkeyhint="search"]')

        search_form.send_keys(text)
        time.sleep(self.sleep_time)
        search_form.send_keys(Keys.ENTER)

    def get_point_data(self, url) -> None:

        self.driver.get(url.get_attribute('href'))
        print(self.driver.find_element(By.CLASS_NAME, '_tvxwjf').text)
        print(self.driver.find_element(By.CLASS_NAME, '_oqoid').text)
        print(self.driver.find_element(By.CLASS_NAME, '_1p8iqzw').text)
        phone_block = self.driver.find_element(By.CLASS_NAME, '_b0ke8')
        phone_block.find_element(By.TAG_NAME, 'button').click()
        time.sleep(self.sleep_time)
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

        # pages_count
        point_count = int(self.driver.find_element(By.CLASS_NAME, "_1xhlznaa").text) // 12

        paginator_next = self.driver.find_element(
            By.CSS_SELECTOR, '._5ocwns > div:nth-child(2) > svg')

        for points_page in range(1, point_count + 1):
            time.sleep(self.sleep_time)
            urls = self.driver.find_elements(By.CSS_SELECTOR, 'div._zjunba > a')

            if len(urls) > 0:
                for url in urls:
                    if url.get_attribute('href'):

                        url = url.get_attribute('href')
                        sub_browser = webdriver.Chrome()
                        sub_browser.get(url)

                        time.sleep(3)

                        # self.driver.find_element(By.CLASS_NAME, "_euwdl0").click()

                        print(sub_browser.find_element(By.CLASS_NAME, '_tvxwjf').text)
                        # print(sub_browser.find_element(By.CLASS_NAME, '_oqoid').text)
                        try:
                            address = sub_browser.find_element(By.CLASS_NAME, '_oqoid')
                        except NoSuchElementException:
                            address = sub_browser.find_element(By.CLASS_NAME, "_er2xx9")
                        print(address.text)
                        print(sub_browser.find_element(By.CLASS_NAME, '_1p8iqzw').text)
                        # phone_block = sub_browser.find_element(By.CLASS_NAME, '_b0ke8')
                        # phone_block.find_element(By.TAG_NAME, 'button').click()
                        # time.sleep(self.sleep_time)
                        # phone = sub_browser.find_element(By.TAG_NAME, 'bdo').text
                        # print(phone)
                        # email = sub_browser.find_element(By.CSS_SELECTOR, 'div._599hh > div:nth-child(4)').text
                        # print(email)
                        time.sleep(self.sleep_time)
                        sub_browser.quit()

            time.sleep(self.sleep_time)

            # scroll_to_points_elements
            actions = ActionChains(self.driver)
            actions.move_to_element(paginator_next).perform()
            paginator_next.click()


if __name__ == '__main__':
    browser = Browser()
    gis_2 = "https://2gis.ru/"
    city = "Набережные Челны"
    search = "Автосервис"
    browser.double_gis_parse_url(gis_2, location=city)
    time.sleep(5)
    browser.driver.close()
