import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class ResultsPage(BasePage):

    RESULTS_LIST = (By.CSS_SELECTOR, "[data-test-id='results-list']")
    TICKET_ITEM = (By.CSS_SELECTOR, "[data-test-id='ticket-item']")
    DIRECT_FLIGHTS_CHECKBOX = (By.CSS_SELECTOR, "[data-test-id='direct-flights-checkbox']")
    DIRECT_FLIGHT_INDICATOR = (By.CSS_SELECTOR, "[data-test-id='direct-flight']")

    @allure.step("Дождаться загрузки результатов")
    def wait_results(self):
        self.wait_visible(self.RESULTS_LIST)

    @allure.step("Применить фильтр 'Только прямые рейсы'")
    def filter_direct(self):
        self.click(self.DIRECT_FLIGHTS_CHECKBOX)

    @allure.step("Проверить что все билеты - прямые рейсы")
    def all_tickets_are_direct(self):
        tickets = self.driver.find_elements(*self.TICKET_ITEM)
        direct_indicators = self.driver.find_elements(*self.DIRECT_FLIGHT_INDICATOR)
        return len(tickets) == len(direct_indicators)
