import allure
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть страницу: {url}")
    def open(self, url: str):
        self.driver.get(url)

    @allure.step("Дождаться видимости элемента: {locator}")
    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Дождаться скрытия элемента: {locator}")
    def wait_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step("Дождаться кликабельности элемента: {locator}")
    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Кликнуть по элементу: {locator}")
    def click(self, locator):
        self.wait_clickable(locator).click()

    @allure.step("Ввести текст '{text}' в поле: {locator}")
    def type(self, locator, text: str):
        elem = self.wait_visible(locator)
        elem.clear()
        elem.send_keys(text)
        elem.send_keys(Keys.RETURN)

    @allure.step("Выполнить JS клик по элементу")
    def execute_js_click(self, element):
        self.driver.execute_script("arguments[0].click();", element)
