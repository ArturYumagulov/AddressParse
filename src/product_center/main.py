import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from sqlalchemy import select, exists

from config.config import DB
from models.address import Address


class ProductCenterParser:

    def __init__(self, region_slug):
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome()
        self.region_slug = f"r-{region_slug}"
        self.map_url = "https://productcenter.ru/map/"
        self.point_url = "https://productcenter.ru/producers/"
        self.coordinates = self.get_coordinates()
        self.db = DB()

    def get_points(self):
        self.driver.get(f"{self.point_url}{self.region_slug}")
        self.driver.implicitly_wait(10)
        address = ""
        region = None
        email = None
        phone = None
        inn = None
        legal_name = None
        point_coordinates = None
        name = None
        locality = None
        street = None

        time.sleep(3)
        firms = self.driver.find_elements(By.CSS_SELECTOR, '.text .link ')
        for card in firms:
            firm_link = card.get_attribute('href')
            print(firm_link)
            point_id = firm_link[8:].split('/')[2]
            exists_query = select(exists().where(Address.point_id == point_id))
            exists_result = self.db.execute(exists_query).scalar()
            print(exists_result)

            if not exists_result:

                point_coordinates = self.coordinates[int(point_id)]
                sub_opt = webdriver.ChromeOptions()
                sub_opt.add_argument('--headless')
                sub_driver = webdriver.Chrome(options=sub_opt)
                sub_driver.get(firm_link)

                contact = sub_driver.find_element(By.CSS_SELECTOR, '.tab_contacts')
                contact.click()

                try:
                    region = sub_driver.find_element(By.CSS_SELECTOR, 'span[itemprop="addressRegion"]').text
                    address += region + ' '
                except NoSuchElementException:
                    pass

                try:
                    locality = sub_driver.find_element(By.CSS_SELECTOR, 'span[itemprop="addressLocality"').text
                    address += locality + ' '
                except NoSuchElementException:
                    pass

                try:
                    street = sub_driver.find_element(By.CSS_SELECTOR, 'span[itemprop="streetAddress"]').text
                    address += street + ' '
                except NoSuchElementException:
                    pass

                try:
                    email = sub_driver.find_element(By.CSS_SELECTOR, 'span[itemprop="email"]').text
                except NoSuchElementException:
                    pass

                try:
                    phone = sub_driver.find_element(By.CSS_SELECTOR, 'span[itemprop="telephone"]').text
                except NoSuchElementException:
                    pass

                try:
                    inn = sub_driver.find_element(By.XPATH,
                                                  '//table[@class="company_data"]//tr[td[text()="ИНН"]]/td[2]').text
                except NoSuchElementException:
                    pass

                try:
                    legal_name = (
                        sub_driver.find_element(By.XPATH,
                                                '//table[@class="company_data"]//tr[td[text()="Наименование"]]/td[2]').text)
                except NoSuchElementException:
                    pass
                try:
                    name = sub_driver.find_element(By.CSS_SELECTOR, '.iv_content h1').text
                except NoSuchElementException:
                    pass

                new_address = {
                    'point_id': point_id,
                    'name': name,
                    'address': address,
                    'request_address': address,
                    'full_address': address,
                    'phone': phone,
                    'email': email,
                    'type': "productcenter.ru",
                    'department': 'b2b',
                    'formatted': address,
                    'province': region,
                    'city': locality,
                    'street': street,
                    'latitude': point_coordinates[0],
                    'longitude': point_coordinates[1],
                    'source_url': firm_link,
                    'inn': inn,
                    'legal_name': legal_name
                }

                print(new_address)

                self.db.add(Address(**new_address))
                self.db.commit()

            time.sleep(3)
        self.db.close()

    def get_coordinates(self):
        """Получение списка координат карты"""

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        url = f'{self.map_url}{self.region_slug}'
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        time.sleep(5)

        map_companies_id = driver.execute_script("return window.map_companies_id;")
        points = driver.execute_script("return points;")
        driver.quit()
        data = zip(map_companies_id, points)
        return dict(data)


if __name__ == '__main__':
    x = ProductCenterParser("tatarstan-riesp-214")
    x.get_points()
    # print(x.get_coordinates())

