import pytest
import requests
import sys
from selenium import webdriver
from pathlib import Path
from datetime import datetime, timedelta
from pages.aviasales_api import AviasalesAPI


project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))


for dir_name in ['pages', 'tests']:
    dir_path = project_root / dir_name
    if dir_path.exists():
        sys.path.insert(0, str(dir_path))


# UI фикстуры
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# API фикстуры
@pytest.fixture
def api():
    return AviasalesAPI()


@pytest.fixture
def api_headers():
    return {
        "Content-Type": "application/json",
        "referer": "https://www.aviasales.ru/",
        "x-origin-cookie": ("crt=361; nuid=cd4a718a-ba65-42f2-9e0d-d6307cad8700; auid=NDhWaWkqN+0ycHRxYW54Ag==;" 
            "marker=direct;" "calendar_redesign_onboarding=1;" "uncheck_hotel_cookie=true;" 
            "cookies_policy=%7B%22accepted%22%3Atrue%2C%22technical%22%3Atrue%2C%22marketing%22%3Atrue%7D;" 
            "_gcl_au=1.1.611138428.1764425226;" 
            "_clck=1obl7bi%5E2%5Eg1f%5E0%5E2159;" 
            "tmr_lvid=8df43ec8992ad32d93eec750e5438a93; tmr_lvidTS=1712792065359;"
            "_ym_uid=1712792065330917266; _ym_d=1764425226; _ym_isad=1;" 
            "_yoid=d2a1bf84-7f1d-40fb-8f29-5f766f4e29a4;"
            "_yosid=ed64ecbf-9e95-4181-90da-b9a218e9252d;" 
            "currency=RUB; _sp_ses.dc27=*;"
            "_awt=393-033299d983566a43c33a6bbb633354626371693576b13d77358f393512f38334d7c2464613b12;" "crt=57;"
            'g_state={"i_l":0,"i_ll":1764456511973,"i_b":"ISTGGvBfINwzQ8XLko6sJyQAdMvveRE2DvklyO9NxH0"};' 
            "tmr_detect=1%7C1764456513012; domain_sid=nDv3QaWCkbng2_aF59Dp4%3A1764456513359;" 
            "_ym_visorc=b;" "_sp_id.dc27=08833d4d-820c-46a7-8712-9d96bbf8270f.1764374508.14.1764456547.1764444650.31019609-b795-4cc6-958c-9648f4fd8f54."
            "9d4b1184-02a3-41aa-b8c0-f0e258487132.91f7957f-3d41-4efd-8d13-b2b50d68ad5b.1764454948251.48")
    }


@pytest.fixture
def base_payload():
    return {
        "search_params": {
            "directions": [],
            "passengers": {
                "adults": 1,
                "children": 0,
                "infants": 0
            },
            "trip_class": "Y"
        },
        "market_code": "ru",
        "marker": "google",
        "citizenship": "RU",
        "currency_code": "rub",
        "languages": {
            "ru": 1
        }
    }


@pytest.fixture
def search_payload(base_payload):
    """Фикстура создаёт валидный payload для поиска туда-обратно"""

    def _create_payload(origin: str, destination: str, date: str):
        payload = base_payload.copy()
        departure_date = datetime.strptime(date, "%Y-%m-%d")
        return_date = departure_date + timedelta(days=7)
        return_date_str = return_date.strftime("%Y-%m-%d")

        payload["search_params"]["directions"] = [
            {
                "origin": origin,
                "destination": destination,
                "date": date,
                "is_origin_airport": False,
                "is_destination_airport": False
            },
            {
                "origin": destination,
                "destination": origin,
                "date": return_date_str,
                "is_origin_airport": False,
                "is_destination_airport": False
            }
        ]
        return payload

    return _create_payload


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

