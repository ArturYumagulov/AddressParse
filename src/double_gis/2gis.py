import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from sqlalchemy import exists

from config.config import DB
from models.address import AddressUrl
from models.schema import AddressUrlSchema


class Browser:
    def __init__(self):
        self.driver: webdriver = webdriver.Chrome()
        self.urls_list = []
        self.sleep_time = 2
        self.db = DB()

    @staticmethod
    def valid_class_content(driver: webdriver, cls: str, res_cls: str):
        try:
            return driver.find_element(By.CLASS_NAME, cls).text
        except NoSuchElementException as ex:
            return driver.find_element(By.CLASS_NAME, res_cls).text

    def search_2gis_form(self, text: str) -> None:
        """Передача данных в поле поиска и нажатие кнопки ENTER"""

        search_form = self.driver.find_element(By.XPATH, '//input[@enterkeyhint="search"]')

        search_form.send_keys(text)
        time.sleep(self.sleep_time)
        search_form.send_keys(Keys.ENTER)

    def get_point_data(self, url: str) -> None:
        """Сбор данных со страницы"""

        sub_browser = webdriver.Chrome()
        sub_browser.get(url)

        time.sleep(self.sleep_time)

        name = self.valid_class_content(sub_browser, "_tvxwjf", "_cwjbox")

        print(name, 'name')

        category = sub_browser.find_element(By.CLASS_NAME, '_1idnaau').text

        print(category, "category")

        address = self.valid_class_content(sub_browser, "_oqoid", "_er2xx9")

        print(address)
        full_address = sub_browser.find_element(By.CLASS_NAME, '_1p8iqzw').text
        print(full_address)

        phone_block = sub_browser.find_element(By.CLASS_NAME, '_b0ke8')

        sub_browser.execute_script("document.querySelector('._1rkbbi0x').scrollTo(0, 300)")
        phone_block.find_element(By.TAG_NAME, 'button').click()
        time.sleep(self.sleep_time)
        phone = sub_browser.find_element(By.TAG_NAME, 'bdo').text

        print(phone)

        email = sub_browser.find_element(By.CSS_SELECTOR, 'div._599hh > div:nth-child(4)').text
        print(email)

        time.sleep(self.sleep_time)
        sub_browser.quit()

    def save_url(self, data: AddressUrlSchema):
        self.db.add(AddressUrl(
            point_id=data.point_id,
            clean_url=data.clean_url,
            city=data.city,
            slug=data.city_slug
        ))
        self.db.commit()

    def double_gis_parse_url(self, url: str, location: str):
        """Парсинг 2GIS. Сбор адресов"""

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
                        full_url = url.get_attribute('href')
                        clean_url = full_url.split('?')[0]
                        parse_url = clean_url.split('/')
                        point_id = parse_url[-1]
                        city_slug = parse_url[3]
                        if self.db.query(exists().where(AddressUrl.point_id == point_id)).scalar():
                            continue
                        else:
                            new_address = AddressUrlSchema(
                                point_id=point_id,
                                clean_url=clean_url,
                                city=location,
                                city_slug=city_slug
                            )

                            self.save_url(new_address)  # сохранение URL в БД
                            self.get_point_data(clean_url)

            time.sleep(self.sleep_time)
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
