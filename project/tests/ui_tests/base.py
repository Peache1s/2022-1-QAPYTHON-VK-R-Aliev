import pytest
from _pytest.fixtures import FixtureRequest
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.main_page import MainPage
import os
import allure
from selenium.webdriver.common.action_chains import ActionChains


class BaseCase:
    driver = None

    @pytest.fixture()
    def login(self):
        self.logger.info("Start")
        return self.login_page.login()

    @pytest.fixture(scope='function', autouse=True )
    def setup(self, driver, request: FixtureRequest, logger):
        self.driver = driver
        self.logger = logger
        self.base_page : BasePage = (request.getfixturevalue('base_page'))
        self.login_page : LoginPage = (request.getfixturevalue('login_page'))
        self.registration_page : RegistrationPage = (request.getfixturevalue('registration_page'))
        self.main_page: MainPage = (request.getfixturevalue('main_page'))
        self.action = ActionChains(self.driver)

    @pytest.fixture(scope='function', autouse=True)
    def log_allure(self, logger, temp_dir):
        yield
        log_file = os.path.join(temp_dir, 'test_info.log' )
        with open(log_file, 'r') as f:
            allure.attach(f.read(), 'test_info.log', allure.attachment_type.TEXT)

    @pytest.fixture(scope='function', autouse=True)
    def ui_report(self, driver, request, temp_dir):
        failed_test_count = request.session.testsfailed
        yield
        if request.session.testsfailed > failed_test_count:
            browser_logs = os.path.join(temp_dir, 'browser.log')
            with open(browser_logs, 'w') as f:
                for i in driver.get_log('browser'):
                    f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
            screenshot_path = os.path.join(temp_dir, 'failed.png')
            driver.get_screenshot_as_file(screenshot_path)
            allure.attach.file(screenshot_path, 'failed.png', allure.attachment_type.PNG)
            with open(browser_logs, 'r') as f:
                allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)