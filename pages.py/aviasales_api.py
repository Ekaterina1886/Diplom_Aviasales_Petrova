import allure
from base_api import BaseAPI


class AviasalesAPI(BaseAPI):

    def __init__(self):
        super().__init__("https://tickets-api.aviasales.ru")

    @allure.step("Запуск поиска билетов")
    def start_search(self, payload: dict, headers: dict):
        return self.post("/search/v2/start", json=payload, headers=headers)