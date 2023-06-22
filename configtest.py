import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from settings import valid_email, valid_password

pytest.driver = webdriver.Chrome()
@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    pytest.driver.maximize_window()
    # Переходим на страницу авторизации
    pytest.driver.get("http://petfriends.skillfactory.ru/login")

    yield

    pytest.driver.quit()


@pytest.fixture()
def go_to_pets_page():
    # неявное ожидание 5 сек при каждом шаге
    pytest.driver.implicitly_wait(5)
    # Вводим email
    pytest.driver.find_element(By.ID, "email").send_keys(valid_email)
    # Вводим пароль
    pytest.driver.find_element(By.ID, "pass").send_keys(valid_password)
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Переходим на страницу со списком питомцев пользователя
    pytest.driver.find_element(By.XPATH, '//a[@href="/my_pets"]').click()
    # явное ожидание 10 сек.
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.ID, "all_my_pets")))