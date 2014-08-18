import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.yield_fixture(scope="session")
def driver():
    browser = webdriver.Firefox()
    yield browser
    browser.quit()


@pytest.fixture(scope="function")
def main_page(driver):
    browser = driver
    browser.get('http://localhost:5000')
    browser.implicitly_wait(3)
    return browser


@pytest.fixture(scope="function")
def home_page(driver):
    browser = driver
    browser.get('http://localhost:5000/home')
    browser.implicitly_wait(3)
    return browser


@pytest.fixture(scope="function")
def district_page(driver):
    browser = driver
    browser.get('http://localhost:5000/district')
    browser.implicitly_wait(3)
    return browser


@pytest.fixture(scope="function")
def demo_page(driver):
    browser = driver
    browser.get('http://localhost:5000/demographics')
    browser.implicitly_wait(3)
    return browser


@pytest.fixture(scope="function")
def school_page(district_page):
    browser = district_page
    inputbox = browser.find_element_by_id("district")
    inputbox.send_keys("Enumclaw School District")
    browser.find_element_by_id("submit").click()
    return browser


@pytest.fixture(scope="function")
def results_page(school_page):
    browser = school_page
    school_inputbox = browser.find_element_by_id("school")
    school_inputbox.send_keys("Enumclaw Middle School")
    number_inputbox = browser.find_element_by_id("numschools")
    number_inputbox.send_keys(10)
    browser.find_element_by_id("grade8").click()
    browser.find_element_by_id("submit").click()
    return browser


def test_front_page(main_page):
    browser = main_page
    assert browser.title == 'School Clustering'
    assert browser.find_element_by_id("start_button")


def test_start_button(main_page):
    browser = main_page
    browser.find_element_by_id("start_button").click()
    assert browser.title == 'Home'
    assert browser.find_element_by_id("choose_school")
    assert browser.find_element_by_id("choose_demo")


def test_base_html_home_link(home_page):
    browser = home_page
    browser.find_element_by_id("home_link").click()
    assert browser.title == "Home"


def test_base_html_about_link(home_page):
    browser = home_page
    browser.find_element_by_id("about_link").click()
    assert browser.title == "About"


def test_home_page_choose_school_button(home_page):
    browser = home_page
    browser.find_element_by_id("choose_school").click()
    assert browser.title == "Select District"


def test_district_page_content(district_page):
    browser = district_page
    assert browser.find_element_by_id("district")
    assert browser.find_element_by_id("submit")


def test_district_submit_no_entry_raise_alert_return_to_page(district_page):
    browser = district_page
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select District"


def test_district_submit_invalid_entry_alert_return_to_page(district_page):
    browser = district_page
    inputbox = browser.find_element_by_id("district")
    inputbox.send_keys("Blarg School District")
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select District"


def test_district_with_entry_submit(district_page):
    browser = district_page
    inputbox = browser.find_element_by_id("district")
    inputbox.send_keys("Enumclaw School District")
    browser.find_element_by_id("submit").click()
    assert browser.title == "Select School"


def test_school_page_content(school_page):
    browser = school_page
    assert browser.find_element_by_css_selector("h1").text == \
        "Enumclaw School District"
    assert browser.find_element_by_id("school")
    assert browser.find_element_by_id("numschools")
    assert browser.find_element_by_name("enrollment")
    assert browser.find_element_by_id("grade3")
    assert browser.find_element_by_id("submit")
    assert browser.find_element_by_id("reset")


def test_school_reset_button(school_page):
    browser = school_page
    browser.find_element_by_id("reset").click()
    assert browser.title == "Select District"


def test_school_submit_no_entry_raise_alert_return_to_page(school_page):
    browser = school_page
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select School"


def test_school_submit_no_number_return_to_page(school_page):
    browser = school_page
    inputbox = browser.find_element_by_id("school")
    inputbox.send_keys("Enumclaw Middle School")
    browser.find_element_by_id("submit").click()
    assert browser.title == "Select School"


def test_school_submit_no_grade_return_to_page(school_page):
    browser = school_page
    school_inputbox = browser.find_element_by_id("school")
    school_inputbox.send_keys("Enumclaw Middle School")
    number_inputbox = browser.find_element_by_id("numschools")
    number_inputbox.send_keys(10)
    browser.find_element_by_id("submit").click()
    assert browser.title == "Select School"


def test_school_submit_invalid_entry_raise_alert_return_to_page(school_page):
    browser = school_page
    inputbox = browser.find_element_by_id("school")
    inputbox.send_keys("Blarg Middle School")
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select School"


def test_school_submit_invalid_number_raise_alert_return_to_page(school_page):
    browser = school_page
    school_inputbox = browser.find_element_by_id("school")
    school_inputbox.send_keys("Enumclaw Middle School")
    number_inputbox = browser.find_element_by_id("numschools")
    number_inputbox.send_keys('10.5')
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select School"


def test_school_invalid_grade_selection(school_page):
    """
    Not yet implemented.
    """
    pass


def test_school_submit_valid_inputs(school_page):
    browser = school_page
    school_inputbox = browser.find_element_by_id("school")
    school_inputbox.send_keys("Enumclaw Middle School")
    number_inputbox = browser.find_element_by_id("numschools")
    number_inputbox.send_keys(10)
    browser.find_element_by_id("grade8").click()
    browser.find_element_by_id("submit").click()
    assert browser.title == "Results"


def test_results_page_content(results_page):
    browser = results_page
    assert browser.find_element_by_id("original_school")
    assert browser.find_element_by_id("target_school").text == \
        "Enumclaw Middle School"
    assert browser.find_element_by_id("final_results")


def test_results_page_dropdowns(results_page):
    browser = results_page
    glyph = browser.find_element_by_xpath("//td[@id='target_school']/span[1]")
    assert not browser.find_element_by_id("4210").is_displayed()
    glyph.click()
    assert browser.find_element_by_id("4210").is_displayed()


def test_home_page_choose_demo_button(home_page):
    browser = home_page
    browser.find_element_by_id("choose_demo").click()
    assert browser.title == "Select Demographics"


def test_demographics_page_content(demo_page):
    browser = demo_page
    assert browser.find_element_by_name("enrollment")
    assert browser.find_element_by_id("grade3")
    assert browser.find_element_by_id("submit")
    assert browser.find_element_by_id("reset")
    assert browser.find_element_by_id("test1")


def test_demo_page_reset(demo_page):
    browser = demo_page
    browser.find_element_by_id("reset").click()
    assert browser.title == "Select Demographics"


def test_demo_page_submit_no_grade_no_score_returns_to_page(demo_page):
    browser = demo_page
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select Demographics"


def test_demo_page_submit_no_grade_returns_to_page(demo_page):
    browser = demo_page
    browser.find_element_by_id("test1").click()
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select Demographics"


def test_demo_page_submit_no_score_returns_to_page(demo_page):
    browser = demo_page
    browser.find_element_by_id("grade7").click()
    browser.find_element_by_id("submit").click()
    assert EC.alert_is_present()
    alert = browser.switch_to_alert()
    alert.accept()
    assert browser.title == "Select Demographics"


def test_demo_page_submit_grade7_reading(demo_page):
    browser = demo_page
    browser.find_element_by_id("grade7").click()
    browser.find_element_by_id("test1").click()
    browser.find_element_by_id("submit").click()
    assert browser.title == "Test Score Histograms for Clusters"


def test_demo_page_submit_grade10_writing(demo_page):
    browser = demo_page
    browser.find_element_by_id("grade10").click()
    browser.find_element_by_id("test2").click()
    browser.find_element_by_id("submit").click()
    assert browser.title == "Test Score Histograms for Clusters"


def test_demo_page_submit_grade5_math(demo_page):
    browser = demo_page
    browser.find_element_by_id("grade5").click()
    browser.find_element_by_id("test3").click()
    browser.find_element_by_id("submit").click()
    assert browser.title == "Test Score Histograms for Clusters"


def test_demo_page_submit_grade5_science(demo_page):
    browser = demo_page
    browser.find_element_by_id("grade5").click()
    browser.find_element_by_id("test4").click()
    browser.find_element_by_id("submit").click()
    assert browser.title == "Test Score Histograms for Clusters"


def test_demo_page_submit_multi_demographics(demo_page):
    browser = demo_page
    browser.find_element_by_name("lowses").click()
    browser.find_element_by_name("per_black").click()
    browser.find_element_by_id("grade5").click()
    browser.find_element_by_id("test4").click()
    browser.find_element_by_id("submit").click()
    assert browser.title == "Test Score Histograms for Clusters"
