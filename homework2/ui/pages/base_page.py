import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ui.locators import locators
from selenium.webdriver.remote.webelement import WebElement
import getpass
FILE_PATH = '/Users/' + getpass.getuser() + '/Desktop/FROG.jpeg'


class BasePage(object):
    locators = locators.BasePageLocators

    def __init__(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @allure.step('Click')
    def click(self, locator, timeout=None) -> WebElement:
        self.find(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    @allure.step('Input')
    def input(self, locator, request, timeout=None):
        elem = self.find(locator, timeout)
        elem.click()
        elem.clear()
        elem.send_keys(request)
        return elem

    @allure.step('Upload')
    def upload(self, locator,  timeout=None, file_path=FILE_PATH):
        self.find(locator, timeout).send_keys(file_path)
