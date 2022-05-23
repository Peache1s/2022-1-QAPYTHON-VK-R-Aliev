import logging
import pytest
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from ui_tests.ui.pages.base_page import BasePage
from ui_tests.ui.pages.login_page import LoginPage
from ui_tests.ui.pages.registration_page import RegistrationPage
from ui_tests.ui.pages.main_page import MainPage
import sys
import os
import shutil
import random
import string
from selenium.webdriver.chrome.options import Options
from ui_tests.ui.pages.login_page import random_string
import pytest
from api.api_client import ApiClient
import pytest
from mysql.mysql_client import MysqlClient

class BadStatusAppCodeException(Exception):
    pass

@pytest.fixture(scope='function')
def api_client() -> ApiClient:
    base_url = 'http://0.0.0.0:8099/'
    if requests.get(base_url+'status').status_code == 200:
        api_client = ApiClient(login='Peache1s', password='0000', base_url=base_url)
    else:
        raise BadStatusAppCodeException
    return api_client

@pytest.fixture()
def driver(config):
    browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    browser.get('http://0.0.0.0:8099/')
    browser.maximize_window()
    yield browser
    browser.quit()

@pytest.fixture(scope='session')
def config():
    return


@pytest.fixture()
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture()
def registration_page(driver):
    return RegistrationPage(driver=driver)


@pytest.fixture()
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture(scope='session')
def base_temp_dir():
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if os.path.exists(base_dir):
         shutil.rmtree(base_dir)
    return base_dir


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerunput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)
    config.base_temp_dir = base_dir


@pytest.fixture(scope='function')
def logger(temp_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    log_file = os.path.join(temp_dir, 'test_info.log')
    log_level = logging.INFO
    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test_info')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

@pytest.fixture()
def name(request):
    if request.param == '':
        return ''
    else:
        return random_string(request.param)

@pytest.fixture()
def surname(request):
    if request.param == '':
        return ''
    else:
        return random_string(request.param)

@pytest.fixture()
def middlename(request):
    if request.param == '':
        return ''
    else:
        return random_string(request.param)

@pytest.fixture()
def username(request):
    if request.param == '':
        return ''
    else:
        return random_string(request.param)

@pytest.fixture()
def email(request):
    if request.param == '':
        return ''
    elif type(request.param) == int:
        return random_string(request.param)
    elif request.param == '@':
        return random_string(5)+'@'
    elif request.param == '@str':
        return random_string(5)+'@'+random_string(4)
    elif request.param == '.':
        return random_string(5) + '@' + random_string(4) + '.'
    elif request.param == 'full':
        return random_string(5) + '@' + random_string(4) + '.' + random_string(2)

@pytest.fixture()
def password(request):
    if request.param == '':
        return ''
    else:
        return random_string(request.param)

@pytest.fixture()
def confirm_password(request):
    if request.param == '':
        return ''
    else:
        return random_string(request.param)

@pytest.fixture(scope='session', autouse=True)
def mysql():
    mysql_client = MysqlClient(user='root', password='0000', db_name='vkeducation')
    mysql_client.connect()
    return mysql_client

@pytest.fixture(scope='session')
def mysql_client( mysql) -> MysqlClient:
    client = mysql
    yield client
    client.connection.close()