import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def get_all_pets_data():
    pets_number = \
        pytest.driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(': ')[1]
    pets = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')
    return [pets_number, pets]


def get_all_pets_attributes():
    images = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/th/img')
    names = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[1]')
    breeds = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[2]')
    ages = pytest.driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr/td[3]')
    return [images, names, breeds, ages]

#Присутствуют все питомцы.
def test_all_pets_displayed(go_to_pets_page):
    pets_number, pets = get_all_pets_data()[0], get_all_pets_data()[1]
    assert int(pets_number) == len(pets)

#Хотя бы у половины питомцев есть фото.
def test_half_pets_have_photo(go_to_pets_page):
    images = get_all_pets_attributes()[0]
    images_count = 0
    for image in images:
        if 'base64' in image.get_attribute('src'):
            images_count = images_count + 1
    assert images_count / len(images) >= 0.5

# У всех питомцев есть имя, возраст и порода.
def test_all_pets_have_attributes(go_to_pets_page):
    names, breeds, ages = get_all_pets_attributes()[1:]
    for i in range(len(names)):
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''

#У всех питомцев разные имена.
def test_all_pets_have_different_names(go_to_pets_page):
    names = get_all_pets_attributes()[1]
    list_names = [name.text for name in names]
    set_names = set(list_names)
    assert len(set_names) == len(list_names)

#В списке нет повторяющихся питомцев.
def test_all_pets_different(go_to_pets_page):
    WebDriverWait(pytest.driver, 10).until(ec.presence_of_element_located((By.XPATH, ".table.table-hover tbody tr")))
    pets_list = [pet.text for pet in get_all_pets_data()[1]]
    pets_set = set(pets_list)
    assert len(pets_set) == len(pets_list)