from selenium.webdriver.common.by import By
from base_page import BasePage
import allure


class ResultsPage(BasePage):

    TICKET = (By.CSS_SELECTOR, "[data-test-id='ticket']")
    DIRECT_FLIGHTS_ONLY = (By.CSS_SELECTOR, "[data-test-id='direct-flights-only']")

    def wait_results(self):
        with allure.step("Ожидаем отображения результатов"):
            self.wait_visible(self.TICKET)

    def filter_direct(self):
        self.click(self.DIRECT_FLIGHTS_ONLY)

    def all_tickets_are_direct(self) -> bool:
        with allure.step("Проверяем, что все билеты прямые"):
            tickets = self.driver.find_elements(*self.TICKET)
            for t in tickets:
                if "без пересадок" not in t.text.lower():
                    return False
            return True
