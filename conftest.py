import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests


@pytest.fixture
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture
def api_base_url():
    return "https://tickets-api.aviasales.ru"


@pytest.fixture
def api_client(api_base_url):
    class ApiClient:
        def __init__(self, base):
            self.base = base

        def post(self, path, json=None):
            return requests.post(f"{self.base}{path}", json=json)

        def get(self, path, params=None):
            return requests.get(f"{self.base}{path}", params=params)

    return ApiClient(api_base_url)
