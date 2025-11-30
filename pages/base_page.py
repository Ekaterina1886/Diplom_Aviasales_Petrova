from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self, url: str):
        with allure.step(f"Открываем страницу: {url}"):
            self.driver.get(url)

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator):
        with allure.step(f"Кликаем по элементу {locator}"):
            self.wait_clickable(locator).click()

    def type(self, locator, text: str):
        with allure.step(f"Вводим '{text}' в поле {locator}"):
            elem = self.wait_visible(locator)
            elem.clear()
            elem.send_keys(text)

    def execute_js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
