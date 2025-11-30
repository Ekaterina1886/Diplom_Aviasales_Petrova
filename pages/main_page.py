import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class MainPage(BasePage):

    ORIGIN = (By.ID, "avia_form_origin-input")
    DESTINATION = (By.ID, "avia_form_destination-input")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CALENDAR_GRID = (By.CSS_SELECTOR, ".rdp")
    HOT_TICKETS_LINK = (By.CSS_SELECTOR, "[data-test-id='hot-tickets-button']")
    SWAP_BUTTON = (By.CSS_SELECTOR, "[data-test-id='round-button']")
    DATE_FIELD = (By.CSS_SELECTOR, "[data-test-id='start-date-field']")
    ENTRY_RULES_BUTTON = (By.XPATH, "//span[contains(text(), 'Правила въезда')]")
    ENTRY_RULES_MODAL = (By.CSS_SELECTOR, "[role='dialog']")
    ENTRY_RULES_POPUP_TITLE = (By.XPATH, "//div[contains(text(), 'Правила въезда в')]")

    @allure.step("Открыть главную страницу")
    def open_main(self):
        self.open("https://www.aviasales.ru/")
        self.wait_visible(self.ORIGIN)

    @allure.step("Установить город отправления: {city}")
    def set_origin(self, city: str):
        self.type(self.ORIGIN, city)

    @allure.step("Установить город назначения: {city}")
    def set_destination(self, city: str):
        self.type(self.DESTINATION, city)

    @allure.step("Получить значение поля отправления")
    def get_origin_value(self):
        return self.driver.find_element(*self.ORIGIN).get_attribute("value")

    @allure.step("Получить значение поля назначения")
    def get_destination_value(self):
        return self.driver.find_element(*self.DESTINATION).get_attribute("value")

    @allure.step("Нажать кнопку поиска")
    def click_search(self):
        self.click(self.SEARCH_BUTTON)

    @allure.step("Поменять города местами")
    def swap_cities(self):
        self.click(self.SWAP_BUTTON)

    @allure.step("Выбрать дату: {date}")
    def select_date(self, date: str):
        self.click(self.DATE_FIELD)

        day_locator = (By.CSS_SELECTOR, f"td[data-day='{date}'] button")

        day_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(day_locator)
        )

        self.driver.execute_script("arguments[0].click();", day_element)

    @allure.step("Переключить сайт на английский язык")
    def change_site_to_english(self):
        self.open("https://www.aviasales.com/")
        self.wait_visible(self.ORIGIN)

    @allure.step("Открыть горячие билеты")
    def open_hot_tickets(self):
        element = self.wait_clickable(self.HOT_TICKETS_LINK)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.execute_js_click(element)

    @allure.step("Нажать на кнопку 'Правила въезда'")
    def click_entry_rules(self):
        entry_rules_btn = self.wait_clickable(self.ENTRY_RULES_BUTTON)
        self.execute_js_click(entry_rules_btn)
        self.wait_visible(self.ENTRY_RULES_MODAL)

    @allure.step("Получить заголовок всплывающего окна правил въезда")
    def get_entry_rules_popup_title(self):
        popup_title_element = self.wait_visible(self.ENTRY_RULES_POPUP_TITLE)
        return popup_title_element.text
