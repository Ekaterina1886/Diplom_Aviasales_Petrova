from selenium.webdriver.common.by import By
from base_page import BasePage
import allure


class MainPage(BasePage):

    # ЛОКАТОРЫ
    ORIGIN = (By.ID, "origin")
    DESTINATION = (By.ID, "destination")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOW_FARE_LINK = (By.LINK_TEXT, "Календарь низких цен")
    SWAP_BUTTON = (By.CSS_SELECTOR, "[data-test-id='swap-button']")
    LANGUAGE_SELECTOR = (By.CSS_SELECTOR, "[data-test-id='language-selector']")
    LANGUAGE_EN = (By.CSS_SELECTOR, "[data-test-id='lang-en']")
    DATE_FIELD = (By.CSS_SELECTOR, "[data-test-id='departure-date-input']")

    def open_main(self):
        self.open("https://www.aviasales.ru/")

    def set_origin(self, city: str):
        self.type(self.ORIGIN, city)

    def set_destination(self, city: str):
        self.type(self.DESTINATION, city)

    def open_calendar(self):
        self.click(self.LOW_FARE_LINK)

    def click_search(self):
        self.click(self.SEARCH_BUTTON)

    def swap_cities(self):
        self.click(self.SWAP_BUTTON)

    def select_date(self, date: str):
        with allure.step(f"Выбираем дату {date}"):
            self.click(self.DATE_FIELD)
            date_locator = (By.CSS_SELECTOR, f"button[data-test-id='date-{date}']")
            self.click(date_locator)

    def change_language_to_english(self):
        self.click(self.LANGUAGE_SELECTOR)
        self.click(self.LANGUAGE_EN)
