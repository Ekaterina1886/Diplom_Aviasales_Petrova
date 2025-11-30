import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def test_aviasales_booking():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.aviasales.ru")

    wait = WebDriverWait(driver, 125)

    # —————————————————————
    # 1) Закрываем cookie-pop-up, если есть
    # —————————————————————
    try:
        btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-id='accept-cookies-button']"))
        )
        btn.click()
    except Exception:
        pass  # если попапа нет — ок

    # —————————————————————
    # 2) Вводим город назначения «Москва»
    # —————————————————————
    # кликаем по контейнеру автокомплита, чтобы input стал активным
    dest_box = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-id='destination-autocomplete']"))
    )
    dest_box.click()

    # находим сам input
    to_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[data-test-id='destination-input']"))
    )
    to_input.clear()
    to_input.click()
    #to_input.send_keys("Москва")
    # ждём, пока появится хотя бы один вариант из подсказки (если есть)

    #$("*[data-test-id='autocomplete-menu'] ul li:first-of-type").click()
    try:
        suggestion = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test-id='autocomplete-menu'] ul li[data-test-id='popular-destination-Москва']"))
        )
        suggestion.click()
    except Exception:
        # fallback: просто enter
        to_input.send_keys(Keys.ENTER)

    # —————————————————————
    # 3) Открываем календарь — выбираем первую доступную дату
    # —————————————————————
     
    calendar_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-id='start-date-field']"))
    )
    calendar_btn.click()

    # Ждём появления дат календаря
   # wait.until(
   #     EC.visibility_of_element_located((By.CSS_SELECTOR, "*[data-day] > button"))
   # )

    # Выбираем любую конкретную дату — например 5 декабря 2025  "[data-day='2025-12-01']"
    date_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-day='2025-12-05']"))
    )

    date_btn.click()

    # Нажимаем кнопку "Найти"
    search_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test-id='form-submit']"))
    )
    
    search_btn.click()

    # —————————————————————
    # 5) Ждём результаты — билет(ы) на странице
    # —————————————————————
    #
    # data-test-id="search-results-items-list"
    #wait.until(
     #   EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test-id='search-results-items-list']")))
    
    results_list = WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='search-results-items-list']")))

    
    assert results_list is not None, "Контейнер результатов не появился"


    driver.quit()

