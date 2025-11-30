import pytest
import allure
from pages.main_page import MainPage
from pages.results_page import ResultsPage
from pages.hot_tickets_page import HotTicketsPage


@pytest.mark.ui
@allure.title("Поиск авиабилетов отображает результаты")
def test_search_flights(driver):
    with allure.step("Инициализировать страницы"):
        main = MainPage(driver)
        results = ResultsPage(driver)

    with allure.step("Выполнить поиск билетов"):
        main.open_main()
        main.set_destination("Сочи")
        main.select_date("2025-12-20")
        main.click_search()

    with allure.step("Проверить что результаты загрузились"):
        results.wait_results()

@allure.title("Проверка отображения правил въезда для Тайланда")
def test_pattaya_entry_rules(driver):
    with allure.step("Инициализировать главную страницу"):
        main = MainPage(driver)

    with allure.step("Выполнить поиск рейсов в Паттайю"):
        main.open_main()
        main.set_destination("Паттайя")

    with allure.step("Кликнуть на 'Правила въезда'"):
        main.click_entry_rules()

    with allure.step("Проверить отображение всплывающего окна с заголовком"):
        popup_title = main.get_entry_rules_popup_title()
        assert "Правила въезда в Тайланд" in popup_title

@allure.title("Горячие билеты открываются")
def test_hot_tickets(driver):
    with allure.step("Инициализировать главную страницу"):
        main = MainPage(driver)

    with allure.step("Открыть главную страницу и горячие билеты"):
        main.open_main()
        main.open_hot_tickets()

    with allure.step("Инициализировать страницу горячих билетов"):
        hot_tickets_page = HotTicketsPage(driver)

    with allure.step("Проверить что страница загружена"):
        assert hot_tickets_page.is_page_loaded()

    with allure.step("Проверить заголовок"):
        title = hot_tickets_page.get_page_title()
        assert "Горячие билеты" in title

@allure.title("Переход на сайт на английском")
def test_change_language(driver):
    with allure.step("Инициализировать главную страницу"):
        main = MainPage(driver)

    with allure.step("Переключить на английскую версию"):
        main.open_main()
        main.change_site_to_english()

    with allure.step("Проверить английский контент"):
        assert "Flights" in driver.page_source


@allure.title("Swap меняет города местами")
def test_swap_cities(driver):
    with allure.step("Инициализировать главную страницу"):
        main = MainPage(driver)

    with allure.step("Установить города и поменять их местами"):
        main.open_main()
        main.set_destination("Владивосток")
        main.swap_cities()

    with allure.step("Проверить что города поменялись"):
        assert main.get_origin_value() == "Владивосток"
