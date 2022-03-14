from homework1.base import BaseClass
from selenium.webdriver.common.keys import Keys
from homework1 import locators
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, StaleElementReferenceException


class TestMyTarget(BaseClass):

    @pytest.mark.UI
    def test_log_in(self):
       self.log_in('some_email@inbox.ru', 'symbols_for_')

    @pytest.mark.UI
    def test_contact_information(self):
        self.log_in('some_email@inbox.ru', 'symbols_for_')
        elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.CONT_INFO_LOCATOR))
        elem.click()
        elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.CONT_NAME_LOCATOR))
        elem.click()
        elem.send_keys(Keys.COMMAND, 'a')
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys("John")
        elem = self.find(locators.CONT_NUMB_LOCATOR)
        elem.click()
        elem.send_keys(Keys.COMMAND, 'a')
        elem.send_keys(Keys.BACKSPACE)
        elem.send_keys("88005553535")
        elem = self.find(locators.CONT_SUBMIT_LOCATOR)
        elem.click()
        assert 'Information saved successfully' in self.driver.page_source

    @pytest.mark.UI
    def test_log_out(self):
        self.log_in('some_email@inbox.ru', 'symbols_for_')
        elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.LOG_OUT_LOCATOR1))
        elem.click()
        i = 0
        while i < 1:
            try:
                elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.LOG_OUT_LOCATOR2))
                elem.click()
                i += 1
                assert self.driver.current_url == 'https://target.my.com/'
            except ElementClickInterceptedException:
                pass
            except StaleElementReferenceException:
                elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.LOG_OUT_LOCATOR1))
                elem.click()



    @pytest.mark.UI
    @pytest.mark.parametrize("test_input, expected", [(locators.STAT_LOCATOR, 'https://target.my.com/statistics'),
                                                      (locators.BILLING_LOCATOR, 'https://target.my.com/billing')])
    def test_param(self, test_input, expected):
        self.log_in('some_email@inbox.ru', 'symbols_for_')
        elem = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(test_input))
        elem.click()
        assert expected in self.driver.current_url























