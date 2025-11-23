from pages.main_page import MainPage
from pages.results_page import ResultsPage
import allure


@allure.title("Поиск авиабилетов отображает результаты")
def test_search_flights(driver):
    main = MainPage(driver)
    results = ResultsPage(driver)

    main.open_main()
    main.set_origin("Москва")
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


@allure.title("Фильтр 'Только прямые рейсы' работает корректно")
def test_direct_flights_filter(driver):
    main = MainPage(driver)
    results = ResultsPage(driver)

    main.open_main()
    main.set_origin("Москва")
    main.set_destination("Санкт-Петербург")
    main.click_search()

    results.wait_results()
    results.filter_direct()

    assert results.all_tickets_are_direct()



@allure.title("Переключение языка сайта работает")
def test_change_language(driver):
    main = MainPage(driver)

    main.open_main()
    main.change_language_to_english()

    assert "Flights" in driver.page_source


@allure.title("Swap меняет города местами")
def test_swap_cities(driver):
    main = MainPage(driver)

    main.open_main()
    main.set_origin("Москва")
    main.set_destination("Сочи")

    main.swap_cities()

    assert main.driver.find_element(*main.ORIGIN).get_attribute("value") == "Сочи"
    assert main.driver.find_element(*main.DESTINATION).get_attribute("value") == "Москва"
