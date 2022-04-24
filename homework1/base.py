import pytest
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import locators
from selenium.webdriver.common.keys import Keys

CLICK_RETRY = 10


class BaseClass:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def click(self, locator):
        for i in range(CLICK_RETRY):
            try:
                elem = self.find(locator)
                elem.click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise

    def find(self, locator):
        return self.driver.find_element(*locator)

    def log_in(self, name, passw):
        elem_for_return = self.find(locators.LOG_IN_LOCATOR)
        self.click(locators.LOG_IN_LOCATOR)
        elem = self.find(locators.NAME_LOCATOR)
        self.click(locators.NAME_LOCATOR)
        elem.clear()
        elem.send_keys(name)
        elem = self.find(locators.PASSW_LOCATOR)
        self.click(locators.PASSW_LOCATOR)
        elem.send_keys(passw)
        elem.send_keys(Keys.ENTER)
        return elem_for_return
