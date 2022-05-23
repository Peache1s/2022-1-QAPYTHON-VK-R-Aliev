import allure
from ui_tests.ui.pages.base_page import BasePage
from ui_tests.ui.locators.locators import LoginPageLocators
from selenium.webdriver.common.keys import Keys
from ui_tests.ui.pages.main_page import MainPage
from ui_tests.ui.pages.registration_page import RegistrationPage
import random
import string

def random_string(length):
    rand = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return rand

class LoginPage(BasePage):
    url = 'http://0.0.0.0:8099/'
    user = 'Peache1s'
    password = '0000'
    locators = LoginPageLocators

    def login(self, login = None, password = None):
        with allure.step("Login"):
            if login == None and password == None:
                login = self.user
                password = self.password
            self.input(LoginPageLocators.LOG_IN_LOCATOR, login, 5)
            elem = self.input(LoginPageLocators.PASSWORD_LOCATOR, password, 5)
            elem.send_keys(Keys.ENTER)
        return (MainPage(self.driver), elem)

    def go_to_registration_page(self):
        with allure.step("Go to the registration page"):
            self.click(LoginPageLocators.REGISTRATION_LOCATOR)
        return RegistrationPage(self.driver)
