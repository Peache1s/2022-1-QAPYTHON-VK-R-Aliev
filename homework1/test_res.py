from selenium.common.exceptions import TimeoutException
from base import BaseClass
import locators
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestMyTarget(BaseClass):

    @pytest.mark.UI
    def test_log_in(self):
        elem = self.log_in('some_email@inbox.ru', 'symbols_for_')
        assert True == WebDriverWait(self.driver, 15).until(EC.invisibility_of_element(elem))

    @pytest.mark.UI
    def test_contact_information(self):
        self.log_in('some_email@inbox.ru', 'symbols_for_')
        elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.CONT_INFO_LOCATOR))
        self.click(locators.CONT_INFO_LOCATOR)
        elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.CONT_NAME_LOCATOR))
        self.click(locators.CONT_NAME_LOCATOR)
        elem.clear()
        elem.send_keys("John")
        elem = self.find(locators.CONT_NUMB_LOCATOR)
        self.click(locators.CONT_NUMB_LOCATOR)
        elem.clear()
        elem.send_keys("88005553535")
        elem = self.find(locators.CONT_SUBMIT_LOCATOR)
        self.click(locators.CONT_SUBMIT_LOCATOR)
        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locators.NOTIFICATION_LOCATOR))
            assert True
        except TimeoutException:
            assert False, "Не сохранено. Не появилось уведомление"

    @pytest.mark.UI
    def test_log_out(self):
        self.log_in('some_email@inbox.ru', 'symbols_for_')
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.LOG_OUT_LOCATOR1))
        self.click(locators.LOG_OUT_LOCATOR1)
        elem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locators.LOG_OUT_LOCATOR2))
        self.click(locators.LOG_OUT_LOCATOR2)
        assert True == WebDriverWait(self.driver, 15).until(EC.invisibility_of_element(element))

    @pytest.mark.UI
    @pytest.mark.parametrize("test_input, expected", [(locators.STAT_LOCATOR, 'Statistics'),
                                                      (locators.BILLING_LOCATOR, 'Billing')])
    def test_param(self, test_input, expected):
        self.log_in('some_email@inbox.ru', 'symbols_for_')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(test_input))
        self.click(test_input)
        assert WebDriverWait(self.driver, 20).until(EC.title_is(expected)) == True
