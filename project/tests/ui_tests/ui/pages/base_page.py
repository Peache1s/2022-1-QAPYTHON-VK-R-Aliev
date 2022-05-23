import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui_tests.ui.locators import locators
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from datetime import datetime


class BasePage(object):
    locators = locators.BasePageLocators

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout = None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Click')
    def click(self, locator, timeout=None) -> WebElement:
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()
        return elem

    @allure.step('Input')
    def input(self, locator, request, timeout=None):
        elem = self.find(locator, timeout)
        elem.click()
        elem.clear()
        elem.send_keys(request)
        return elem


    def elem_is_invisible(self, element,  timeout=None):
        return self.wait(timeout).until(EC.invisibility_of_element(element))

    def elem_visible(self, locator):
        try:
            self.find(locator)
            return True
        except TimeoutException:
            return False

    def wait_text_in_error_flash(self, locator, message):
        try:
            start_time = datetime.now().second
            while True:
                locator_text = self.find(locator).text
                if locator_text ==  message:
                    break
                delta_time = datetime.now().second - start_time
                if delta_time >= 2:
                    break
            return locator_text
        except TimeoutException:
            return False
