import time

from selenium import webdriver
from selenium.webdriver.common.by import By


class TorgBox:
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.url = url
        self.links = []
        self.page_count = 0

    def authorize(self, login, password):
        login_input = self.driver.find_element(By.ID, 'email')
        login_input.send_keys(login)

        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys(password)

        button = self.driver.find_element(By.CSS_SELECTOR, 'button[name="submit"]')
        button.click()

    def get_cards(self):
        result = []
        cards = self.driver.find_elements(By.CSS_SELECTOR, '.entity-name-link')
        for card in cards:
            result.append(card.get_attribute('href'))
        return result

    def parse(self):
        self.driver.get(self.url)
        self.driver.implicitly_wait(10)
        popup = self.driver.find_element(By.CSS_SELECTOR, '.button_inverted')
        time.sleep(5)
        popup.click()

        self.authorize("topb2b@tranzit-oil.com", "mazda387")
        self.driver.implicitly_wait(10)

        self.driver.get('https://torgbox.ru/contragents/search')

        time.sleep(60)
        self.page_count = int(
            self.driver.find_element(By.CSS_SELECTOR,
                                     'ul.pagination li:not(.pagination__item--next):nth-last-child(2) a').text)
        for page in range(1, self.page_count + 1):
            print('sleep')
            time.sleep(10)
            cards = self.get_cards()
            print(cards)
            self.links.extend(cards)
            self.driver.execute_script(
                "document.querySelector('.pagination-wrapper').scrollIntoView({behavior: 'smooth'})")
            next_page = self.driver.find_element(By.CLASS_NAME, 'pagination__link--next')
            next_page.click()

        print(self.links)
        time.sleep(5)

        time.sleep(60)


if __name__ == '__main__':
    x = TorgBox('https://torgbox.ru/login')
    x.parse()