import pytest
import locators
from selenium.webdriver.common.keys import Keys

class BaseClass:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def click(self, locator):
        elem = self.find(locator)
        elem.click()

    def find(self, locator):
        return self.driver.find_element(*locator)

    def log_in(self, name, passw):
        elem = self.find(locators.LOG_IN_LOCATOR)
        elem.click()
        elem = self.find(locators.NAME_LOCATOR)
        elem.click()
        elem.send_keys(name)
        elem = self.find(locators.PASSW_LOCATOR)
        elem.click()
        elem.send_keys(passw)
        elem.send_keys(Keys.ENTER)
        assert 'Invalid login or password' not in self.driver.page_source


