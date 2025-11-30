import pytest
import allure


@allure.feature("Поиск билетов")
@allure.story("Успешный поиск")
@pytest.mark.parametrize(
    "origin,destination,date",
    [
        ("BEG", "MOW", "2025-12-14"),
        ("BEG", "LED", "2025-12-01"),
        ("BEG", "KGD", "2025-12-12"),
    ]
)
def test_search_success(api, api_headers, search_payload, origin, destination, date):
    payload = search_payload(origin, destination, date)

    resp = api.start_search(payload, api_headers)

    assert resp.status_code == 200
    data = resp.json()
    assert "search_id" in data
    assert isinstance(data["search_id"], str)
    assert len(data["search_id"]) > 0


@allure.feature("Поиск билетов")
@allure.story("Структура ответа")
def test_response_structure(api, api_headers, search_payload):
    payload = search_payload("BEG", "MOW", "2025-12-14")

    resp = api.start_search(payload, api_headers)

    assert resp.status_code == 200
    data = resp.json()

    assert "search_id" in data
    assert "places" in data
    assert "currency_rates" in data
    assert "results_url" in data


@allure.feature("Ошибки API")
@allure.story("Неправильный формат даты")
def test_invalid_date(api, api_headers, base_payload):
    payload = base_payload.copy()
    payload["search_params"]["directions"] = [
        {
            "origin": "BEG",
            "destination": "MOW",
            "date": "31-12-2025",
            "is_origin_airport": False,
            "is_destination_airport": False
        }
    ]
    resp = api.start_search(payload, api_headers)

    assert resp.status_code in [400, 422]


@allure.feature("Ошибки API")
@allure.story("Отсутствуют обязательные поля")
def test_missing_required_fields(api, api_headers):
    incomplete_payload = {
        "market_code": "ru",
        "marker": "google",
        "citizenship": "RU",
        "currency_code": "rub",
        "languages": {
            "ru": 1
        }
    }
    resp = api.start_search(incomplete_payload, api_headers)

    assert resp.status_code in [400, 422, 500]


@allure.feature("Поиск билетов")
@allure.story("Мультисегментный поиск")
def test_multiple_segments(api, api_headers, base_payload):
    payload = base_payload.copy()
    payload["search_params"]["directions"] = [
        {
            "origin": "BEG",
            "destination": "IST",
            "date": "2025-12-20",
            "is_origin_airport": False,
            "is_destination_airport": False
        },
        {
            "origin": "IST",
            "destination": "BKK",
            "date": "2025-12-25",
            "is_origin_airport": False,
            "is_destination_airport": False
        }
    ]
    resp = api.start_search(payload, api_headers)

    assert resp.status_code == 200
    assert "search_id" in resp.json()


