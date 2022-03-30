from ui.pages.base_page import BasePage
from ui.locators.locators import LoginPageLocators
from selenium.webdriver.common.keys import Keys
from ui.pages.campaign_page import CampaignPage
from selenium.webdriver.support import expected_conditions as EC
import random
import string


def random_number(length):
    rand = ''.join(str(random.randint(0, 9)) for i in range(length))
    return rand


def random_string(length):
    rand = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return rand


class LoginPage(BasePage):
    url = 'https://target.my.com/'
    user = 'some_email@inbox.ru'
    password = 'symbols_for_'
    locators = LoginPageLocators

    def login(self):
        self.click(LoginPageLocators.LOG_IN_LOCATOR, 5)
        self.input(LoginPageLocators.NAME_LOCATOR, self.user, 5)
        elem = self.input(LoginPageLocators.PASSW_LOCATOR, self.password, 5)
        elem.send_keys(Keys.ENTER)
        return CampaignPage(self.driver)

    def elem_is_visible(self, element,  timeout=None):
        return self.wait(timeout).until(EC.visibility_of(element))
