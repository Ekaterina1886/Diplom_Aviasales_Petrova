import pytest
import allure
from pages.main_page import MainPage
from pages.results_page import ResultsPage


@pytest.mark.ui
@allure.title("Поиск авиабилетов отображает результаты")
def test_search_flights(driver):
    main = MainPage(driver)
    results = ResultsPage(driver)

    main.open_main()
    main.set_origin("Белград")
    main.set_destination("Сочи")
    main.select_date("2025-12-20")
    main.click_search()

    results.wait_results()


@allure.title("Календарь низких цен открывается")
def test_low_fare_calendar(driver):
    main = MainPage(driver)

    main.open_main()
    main.open_calendar()

    assert "calendar" in driver.current_url


@allure.title("Фильтр 'Без пересадок' работает корректно")
def test_direct_flights_filter(driver):
    main = MainPage(driver)
    results = ResultsPage(driver)

    main.open_main()
    main.set_origin("Белград")
    main.set_destination("Санкт-Петербург")
    main.click_search()

    results.wait_results()
    results.filter_direct()

    assert results.all_tickets_are_direct()


@allure.title("Переключение языка сайта работает")
def test_change_language(driver):
    main = MainPage(driver)

    main.open_main()
    main.change_site_to_english()

    assert "Flights" in driver.page_source


@allure.title("Swap меняет города местами")
def test_swap_cities(driver):
    main = MainPage(driver)

    main.open_main()
    main.set_origin("Белград")
    main.set_destination("Сочи")

    main.swap_cities()

    origin_value = main.driver.find_element(*main.ORIGIN).get_attribute("value")
    destination_value = main.driver.find_element(*main.DESTINATION).get_attribute("value")

    assert origin_value == "Сочи"
    assert destination_value == "Белград"