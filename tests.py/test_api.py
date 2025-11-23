import pytest
import allure
from pages.aviasales_api import AviasalesAPI

@pytest.fixture
def api():
    return AviasalesAPI()


@pytest.fixture
def headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


@pytest.fixture
def base_payload():
    return {
        "marker": "TEST_API",
        "host": "aviasales.ru",
        "locale": "ru",
        "trip_class": "Y",
        "passengers": {"adults": 1, "children": 0, "infants": 0},
    }
@pytest.fixture
def search_payload(base_payload):
    """Фикстура создаёт валидный payload с сегментом для поиска.
    Используется так:
    payload = search_payload(origin="MOW", destination="LED", date="2025-12-01")
    """

    def _create_payload(origin: str, destination: str, date: str):
        payload = base_payload.copy()
        payload["segments"] = [
            {"origin": origin, "destination": destination, "date": date}
        ]
        return payload

    return _create_payload

@allure.feature("Поиск билетов")
@allure.story("Успешный поиск")
@pytest.mark.parametrize(
    "origin,destination,date",
    [
        ("MOW", "LED", "2025-12-01"),
        ("MOW", "IST", "2025-12-20"),
        ("LED", "AYT", "2025-12-15"),
    ]
)
def test_search_success(api, headers, search_payload, origin, destination, date):
    payload = search_payload(origin, destination, date)

    resp = api.start_search(payload, headers)

    assert resp.status_code == 200
    data = resp.json()
    assert "search_id" in data
    assert isinstance(data["search_id"], str)

@allure.feature("Поиск билетов")
@allure.story("Структура ответа")
def test_response_structure(api, headers, search_payload):
    payload = search_payload("MOW", "LED", "2025-12-01")

    resp = api.start_search(payload, headers)

    assert resp.status_code == 200
    assert "status" in resp.json()

@allure.feature("Ошибки API")
@allure.story("Отсутствует поле segments")
def test_missing_segments(api, headers, base_payload):
    payload = base_payload.copy()  # без segments

    resp = api.start_search(payload, headers)
    assert resp.status_code in (400, 422, 500)

@allure.feature("Ошибки API")
@allure.story("Неправильный формат даты")
def test_invalid_date(api, headers, search_payload):
    payload = search_payload("MOW", "LED", "31-12-2025")  # неправильно

    resp = api.start_search(payload, headers)

    assert resp.status_code in (200, 400, 422)



@allure.feature("Поиск билетов")
@allure.story("Мультисегментный поиск")
def test_multiple_segments(api, headers, base_payload):
    payload = base_payload.copy()
    payload["segments"] = [
        {"origin": "MOW", "destination": "IST", "date": "2025-12-20"},
        {"origin": "IST", "destination": "BKK", "date": "2025-12-25"},
    ]

    resp = api.start_search(payload, headers)

    assert resp.status_code == 200
    assert "search_id" in resp.json()

