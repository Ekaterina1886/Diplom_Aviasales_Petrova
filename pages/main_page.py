import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class MainPage(BasePage):

    ORIGIN = (By.ID, "avia_form_origin-input")
    DESTINATION = (By.ID, "avia_form_destination-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOW_FARE_LINK = (By.LINK_TEXT, "Календарь низких цен")
    SWAP_BUTTON = (By.CSS_SELECTOR, "[data-test-id='round-button']")
    LANGUAGE_SELECTOR = (By.CSS_SELECTOR, "[data-test-id='language-selector']")
    LANGUAGE_EN = (By.CSS_SELECTOR, "[data-test-id='lang-en']")
    DATE_FIELD = (By.CSS_SELECTOR, "[data-test-id='start-date-field']")

    def open_main(self):
        self.open("https://www.aviasales.ru/")
        self.wait_visible(self.ORIGIN)

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
            calendar_grid = (By.CSS_SELECTOR, ".rdp")
            self.wait_visible(calendar_grid)
            date_locator = (By.CSS_SELECTOR, f"td[data-day='{date}'] button")
            element = self.wait_visible(date_locator)
            self.execute_js_click(element)

    def change_site_to_english(self):
        self.open("https://www.aviasales.com/")

