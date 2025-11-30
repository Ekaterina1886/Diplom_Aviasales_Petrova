import requests
import allure


class BaseAPI:
    """Базовый API-класс с общими методами"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    @allure.step("POST запрос: {endpoint}")
    def post(self, endpoint: str, json: dict, headers: dict):
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, json=json, headers=headers)

        allure.attach(
            str(json),
            name="Request JSON",
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.JSON
        )

        return response
