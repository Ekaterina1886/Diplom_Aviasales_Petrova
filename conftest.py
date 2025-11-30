import pytest
import requests
import sys
from selenium import webdriver
from pathlib import Path
from datetime import datetime, timedelta
from pages.aviasales_api import AviasalesAPI
from selenium.webdriver.chrome.options import Options


project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))


for dir_name in ['pages', 'tests']:
    dir_path = project_root / dir_name
    if dir_path.exists():
        sys.path.insert(0, str(dir_path))


# UI фикстуры
@pytest.fixture
def driver():
    chrome_options = Options()

   # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# API фикстуры
@pytest.fixture
def api():
    return AviasalesAPI()

@pytest.fixture(scope="session")
def fresh_cookies():
    return (
        "auid=RjVTS2j8ep5KazZQSXVCAg==; currency=rub; marker=google; "
        "nuid=9910378b-2374-4a44-96c6-854091cf4fef; _gcl_au=1.1.1483070304.1761376950; "
        "uxs_uid=66274390-b173-11f0-9310-3bca47a2b934; _yoid=896bd87e-4c89-4281-85f3-100c175e8a7e; "
        "_ym_uid=1761376950209420059; _ym_d=1764438879; tmr_lvid=5baa609772580749088b00a599fc53e8; "
        "tmr_lvidTS=1761376950346; _ym_isad=1; domain_sid=vh0OrIBRZ9xEHWWYZIaxj%3A1764438909439; "
        "cookies_policy=%7B%22accepted%22%3Atrue%2C%22technical%22%3Atrue%2C%22marketing%22%3Atrue%7D; "
        "calendar_redesign_onboarding=1; uncheck_hotel_cookie=true; _yosid=6d6af329-338c-4928-951a-df7907eae215; "
        "currency=rub; carrotquest_device_guid=80aca490-212f-4ca2-917c-108bddbbccee; "
        "carrotquest_uid=2116786155457347754; "
        "carrotquest_auth_token=user.2116786155457347754.29973-d9e118c419c052de7f78078232.86254de189b7529c68ae03feb1fe11f4115c170e98417928; "
        "carrotquest_realtime_services_transport=wss; _sp_ses.dc27=*; _clck=1fp2zp8%5E2%5Eg1g%5E0%5E2124; "
        "_ym_visorc=b; _awt=5c8336ae8386-a83336533671569e66cd36440373322c3667764ebd37369624364633e41865327338; "
        'g_state={"i_l":0,"i_ll":1764500526149,"i_b":"vqLekoQ/6il26/Z6NJ7Eu5JoD/C+WhPzjd8K+pn1D/M"}; '
        "_clsk=10nzid0%5E1764500527548%5E3%5E1%5El.clarity.ms%2Fcollect; tmr_detect=0%7C1764500529317; "
        "_sp_id.dc27=835fed58-46bc-4942-a680-0b1893e08a37.1761376949.9.1764500545.1764454110.9b09ed80-ddd7-4c16-af42-0835d443be24.978ba46a-afce-49b1-a19d-062692f8f368.e40e9051-972a-4a08-a967-19146a5191b4.1764494317620.150; "
        "search_init_stamp=1764500665766"
    )

@pytest.fixture
def api_headers(fresh_cookies):
    return {
        "Content-Type": "application/json",
        "referer": "https://www.aviasales.ru/",
        "x-origin-cookie": fresh_cookies
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
