import allure
from selenium.webdriver.common.by import By
from .base_page import BasePage


class HotTicketsPage(BasePage):

    PAGE_HEADER = (By.CSS_SELECTOR, "h2[data-test-id='brand-text']")

    def __init__(self, driver):
        super().__init__(driver)
        self.wait_visible(self.PAGE_HEADER)

    @allure.step("Проверить что страница горячих билетов загружена")
    def is_page_loaded(self):
        header = self.wait_visible(self.PAGE_HEADER)
        return header.is_displayed() and "Горячие билеты" in header.text

    @allure.step("Получить заголовок страницы")
    def get_page_title(self):
        return self.wait_visible(self.PAGE_HEADER).text
