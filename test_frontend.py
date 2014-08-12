import pytest
from selenium import webdriver


@pytest.yield_fixture
def driver():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


def test_front_page(driver):
    browser = driver
    browser.get('http://localhost:5000')
    browser.implicitly_wait(3)
    assert browser.title == 'School Clustering'
    assert browser.find_element_by_id("start_button")


def test_start_button(driver):
    browser = driver
    browser.get('http://localhost:5000')
    browser.implicitly_wait(3)
    browser.find_element_by_id("start_button").click()
    assert browser.title == 'Home'
