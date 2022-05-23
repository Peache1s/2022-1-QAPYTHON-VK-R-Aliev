from ui_tests.ui.pages.base_page import BasePage
from ui_tests.ui.locators.locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as EC


class MainPage(BasePage):
    locators = MainPageLocators

    def check_title(self, expected_title):
        return self.wait().until(EC.title_is(expected_title))
