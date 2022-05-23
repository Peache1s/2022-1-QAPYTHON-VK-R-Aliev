from ui_tests.ui.pages.base_page import BasePage
from ui_tests.ui.locators.locators import RegistrationPageLocators
import ui_tests.ui.pages.login_page as lp


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators

    def registration(self, name = None, surname = None, middlename = None, username = None, email = None, password = None, confirm_password = None, accept = True):
        if name == None:
            name = lp.random_string(10)
        if surname == None:
            surname = lp.random_string(10)
        if middlename == None:
            middlename = lp.random_string(10)
        if username == None:
            username = lp.random_string(6)
        if email==None:
            email = lp.random_string(7)+'@'+lp.random_string(4)+'.'+lp.random_string(2)
        if password == None:
            password = lp.random_string(8)
            confirm_password = password
        if confirm_password == None:
            confirm_password = password
        self.input(RegistrationPageLocators.NAME_LOCATOR, name)
        self.input(RegistrationPageLocators.SURNAME_LOCATOR, surname)
        self.input(RegistrationPageLocators.MIDDLENAME_LOCATOR, middlename)
        self.input(RegistrationPageLocators.USERNAME_LOCATOR, username)
        self.input(RegistrationPageLocators.EMAIL_LOCATOR, email)
        self.input(RegistrationPageLocators.PASSWORD_LOCATOR, password)
        self.input(RegistrationPageLocators.CONFIRM_PASSWORD_LOCATOR, confirm_password)
        if accept == True:
            self.click(RegistrationPageLocators.REGISTRATION_ACCEPT)
        element = self.click(RegistrationPageLocators.REGISTRATION_BUTTON_LOCATOR)
        return element
