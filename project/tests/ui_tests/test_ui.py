import allure
import pytest
from base import BaseCase
from ui.locators.locators import LoginPageLocators, MainPageLocators, RegistrationPageLocators
from ui.pages.login_page import random_string

@pytest.mark.ui_login
@allure.feature("Log in")
class TestLogin(BaseCase):

    validation_empty_field = "Заполните это поле."
    validation_username = "Минимально допустимое количество символов: 6. Длина текста сейчас: 5."
    username = 'Test'
    password = 'TestPassword'
    @allure.description("""
    Негативный тест логина.
    В качестве пароля и логина вводятся случайные строки.
    Проверка видимости всплывающей ошибки авторизации на странице.
    """
    )
    def test_negative_log_in(self):
        self.logger.info("Start")
        with allure.step('Login with random data'):
            self.login_page.login(random_string(10), random_string(10))
        with allure.step('Assert'):
            self.logger.info("End")
            assert self.login_page.elem_visible(LoginPageLocators.ERROR_LOG_IN_LOCATOR) == True

    @allure.description("""
    Логинится в приложение с логином и паролем, являющимися атрибутами класса LoginPage ( класс страницы авторизации, изначально в нем указан существущий пользователь)
    Проверка пропадания элемента авторизации пользователя  
    """)
    def test_login(self, login):
        with allure.step('Assert'):
            log_in_element = login[1]
            self.logger.info("End")
            assert self.login_page.elem_is_invisible(log_in_element) == True

    @allure.description("""
    Параметризованный тест логина.
    Проверяет валидацию полей:
    -пустое поле логина
    -пустое поле пароля
    -логин менее 6 символов
    Проверка возникающего сообщения
    """)
    @pytest.mark.parametrize("test_login, test_password, input_locator, expected_result", [('', password,LoginPageLocators.LOG_IN_LOCATOR,validation_empty_field ),
                                                           (username, '', LoginPageLocators.PASSWORD_LOCATOR, validation_empty_field),
                                                           (username, password, LoginPageLocators.LOG_IN_LOCATOR, 'validation_username' ),
                                                           ])
    def test_negative_validation_login(self, test_login, test_password, input_locator, expected_result):
        self.logger.info("Start")
        self.login_page.login(test_login, test_password)
        with allure.step("Find message and assert"):
            if expected_result == 'validation_username':
                expected_result = "Минимально допустимое количество символов: 6. Длина текста сейчас: 4."
            self.logger.info("End")
            assert self.login_page.find(input_locator).get_attribute('validationMessage') == expected_result

@pytest.mark.ui_registration
@allure.feature("Registration")
class TestRegistration(BaseCase):

    validation_empty_field = "Заполните это поле."
    validation_username = "Минимально допустимое количество символов: 6. Длина текста сейчас: 5."
    name = 'Test'
    surname = 'Test'
    middlename = 'Test'
    username = 'TestUsr'
    email = 'test@mail.ru'
    password = 'sometestpass'

    @allure.description("""
    Регистрация пользователя с рандомными значениями
    Проверка видимости кнопки регистрации
    """)
    def test_registration(self):
        self.logger.info("Start")
        reg_page = self.login_page.go_to_registration_page()
        with allure.step('Registration'):
            reg_page.registration()
        self.logger.info("End")
        with allure.step('Assert'):
            assert reg_page.elem_is_invisible(RegistrationPageLocators.REGISTRATION_BUTTON_LOCATOR, 5)==True

    @allure.description("""
    Регистрация пользователя с невалидными данными:
    -отсутсвие имени
    -отсутсвие фамилии
    -имя пользователя меньше 6 символов
    -невалидный email
    Проверка валидационного сообщения
    """)
    @pytest.mark.parametrize("name, surname, middlename, username, email, password, confirm_password, input_locator, expected_result", [
        ('',surname, middlename, username, email, password, password, RegistrationPageLocators.NAME_LOCATOR, validation_empty_field),
        (name, '', middlename, username, email, password, password, RegistrationPageLocators.SURNAME_LOCATOR, validation_empty_field),
        (name, surname, middlename, '5symb', email, password, password, RegistrationPageLocators.USERNAME_LOCATOR,'validation_username' ),
        (name, surname, middlename, username, 'email', password, password, RegistrationPageLocators.EMAIL_LOCATOR, 'validation_username')

    ])
    def test_negative_validation_registration(self, name, surname, middlename, username, email, password, confirm_password, input_locator, expected_result):
        self.logger.info("Start")
        self.login_page.go_to_registration_page()
        with allure.step('Registration'):
            self.registration_page.registration(name, surname, middlename, username, email, password, confirm_password)
            if expected_result == 'validation_username':
                expected_result = "Минимально допустимое количество символов: 6. Длина текста сейчас: 5."
        with allure.step('Assert'):
            assert self.registration_page.find(input_locator).get_attribute('validationMessage') == expected_result

    @allure.description("""
    Регистрация с непроставленным чекбоксом.
    Проверка возникающего валидационного сообщения
    """)
    def test_negative_checkbox(self):
        self.logger.info("Start")
        self.login_page.go_to_registration_page()
        with allure.step('Registration'):
            self.registration_page.registration(random_string(10), random_string(10), random_string(10), random_string(6),random_string(6)+'@mail.ru', self.password, self.password, False)
        with allure.step('Assert'):
            self.logger.info("End")
            assert self.registration_page.find(RegistrationPageLocators.REGISTRATION_ACCEPT).get_attribute('validationMessage') == 'Чтобы продолжить, установите этот флажок.'


    @allure.description("""
    Проверка регистрации пользователя с неподходящими под формат почтой и несовпадающими пароялми:
    Проверяется всплывающее сообщение
    """)
    @pytest.mark.parametrize("email, password, confirm_password, expected_result", [
        ('testing', password, password, 'Invalid email address'),
        ('testing@', password, password,'Invalid email address'),
        ('test@mail', password, password, 'Invalid email address'),
        ('test@mail.', password, password, 'Invalid email address'),
        (email, '112','111', 'Passwords must match'),
        ('test', '112', '111', 'Invalid email address\nPasswords must match')
        ])
    def test_negative_email_and_passwords(self, email, password, confirm_password, expected_result):
        self.logger.info("Start")
        self.login_page.go_to_registration_page()
        with allure.step("Registration"):
            self.registration_page.registration(random_string(10),random_string(10), random_string(10), random_string(6), email, password, confirm_password)
        with allure.step('Assert'):
            self.logger.info("End")
            assert self.registration_page.wait_text_in_error_flash(RegistrationPageLocators.ERROR_LOCATOR, expected_result) == expected_result

    @allure.description("""
    Тест создания пользователя с существующим именем пользователя
    Проверка появления ошибки ошибки
    """)
    def test_negative_create_existing_usr(self):
        username = random_string(10)
        self.logger.info("Start")
        self.login_page.go_to_registration_page()
        with allure.step('Registration new user and logout'):
            self.registration_page.registration(username=username)
            self.main_page.click(MainPageLocators.LOG_OUT_LOCATOR)
        with allure.step('Registration user with existing username'):
            self.login_page.go_to_registration_page()
            self.registration_page.registration(username=username)
        with allure.step('Assert'):
            self.logger.info("End")
            assert self.registration_page.wait_text_in_error_flash(RegistrationPageLocators.ERROR_LOCATOR,'User already exist')

@pytest.mark.ui_main_page
@allure.feature("MainPage")
class TestMain(BaseCase):

    @allure.description("""
    Тест на кнопку логаут главной страницы.
    Проверяет отсуствие кнопки логаута
    """)
    def test_logout(self, login):
        with allure.step("Logout"):
            element = self.main_page.click(MainPageLocators.LOG_OUT_LOCATOR)
        self.logger.info("End")
        with allure.step("Assert"):
            assert self.main_page.elem_is_invisible(element) == True


    @allure.description("""
    Тест на кнопку перехода на python.org в верхнем хабе страницы.
    Провека title итоговой страицы.
    """)
    def test_pyton_button(self, login):
        with allure.step('Python click'):
            self.main_page.click(MainPageLocators.PYTHON_LIST_LOCATOR)
        with allure.step('Assert'):
            self.logger.info("End")
            assert self.main_page.check_title('Welcome to Python.org') == True

    @allure.description("""
    Параметризованный тест на кнопки API, Future of the Internet, SMTP.
    Провека title итоговой страицы.
    """)
    @pytest.mark.parametrize("locator, expected_result", [
        (MainPageLocators.API_LOCATOR,'API - Wikipedia' ),
        (MainPageLocators.FUTURE_LOCATOR,'Future of the Internet | How the Internet Will Be in 50 Years'),
        (MainPageLocators.SMTP_LOCATOR, 'SMTP — Википедия')
                                                       ])
    def test_central_links(self, login, locator, expected_result):
        with allure.step(f'Go to {expected_result}'):
            self.main_page.click(locator)
            window_after = self.main_page.driver.window_handles[1]
            self.main_page.driver.switch_to.window(window_after)
        with allure.step('Assert'):
            self.logger.info("End")
            assert self.main_page.check_title(expected_result) == True

    @allure.description("""
    Тестирование ссылок в списке Python
    Провека title итоговой страицы.
    """)
    @pytest.mark.parametrize("locator, expected_result", [
        (MainPageLocators.HISTORY_OF_PYTHON_LOCATOR, 'History of Python - Wikipedia'),
        (MainPageLocators.ABOUT_FLASK_LOCATOR, 'Welcome to Flask — Flask Documentation (1.1.x)')
    ])
    def test_python_list(self, login,locator,expected_result):
        with allure.step("find and click"):
            element = self.main_page.find(MainPageLocators.PYTHON_LIST_LOCATOR)
            self.action.move_to_element(element).perform()
            self.main_page.click(locator)
            if len(self.driver.window_handles) > 1:
                window_after = self.main_page.driver.window_handles[1]
                self.main_page.driver.switch_to.window(window_after)
        with allure.step("Assert"):
            self.logger.info("End")
            assert self.main_page.check_title(expected_result) == True

    @allure.description("""
     Тестирование ссылок в списке Linux
     Провека title итоговой страицы.
     """)
    def test_linux(self, login):
        with allure.step("find and click"):
            element = self.main_page.find(MainPageLocators.LINUX_LOCATOR)
            self.action.move_to_element(element).perform()
            self.main_page.click(MainPageLocators.CENTOS_LOCATOR)
            if len(self.driver.window_handles) > 1:
                window_after = self.main_page.driver.window_handles[1]
                self.main_page.driver.switch_to.window(window_after)
        with allure.step('Assert'):
            self.logger.info("End")
        assert self.main_page.check_title('Загрузить Fedora Workstation') == True

    @allure.description("""
     Тестирование ссылок в списке Network
     Провека title итоговой страицы.
     """)
    @pytest.mark.parametrize("locator, expected_result", [
        (MainPageLocators.WIRESHARK_NEWS_LOCATOR, 'Wireshark · News'),
        (MainPageLocators.WIRESHARK_DOWNLOAD_LOCATOR, 'Wireshark · Go Deep.'),
        (MainPageLocators.TCPDUMP_EXAMPLES_LOCATOR, 'Tcpdump Examples - 22 Tactical Commands | HackerTarget.com')
    ])
    def test_network_list(self, login, locator,expected_result):
        with allure.step("find and click"):
            element = self.main_page.find(MainPageLocators.NETWORK_LOCATOR)
            self.action.move_to_element(element).perform()
            self.main_page.click(locator)
            if len(self.driver.window_handles) > 1:
                window_after = self.main_page.driver.window_handles[1]
                self.main_page.driver.switch_to.window(window_after)
        with allure.step('Assert'):
            self.logger.info("End")
            assert self.main_page.check_title(expected_result) == True

    @allure.description("""
     Тестирование кнопки home и значка debug для обновления страницы
     Провека рандомного факта python внизу страницы
     """)
    @pytest.mark.parametrize("locator", [
        (MainPageLocators.BUG_PICTURE_LOCATOR),
        (MainPageLocators.HOME_LOCATOR)
    ])
    def test_refresh_by_home_and_picture(self, login, locator):
        with allure.step("find and click"):
            python_fact_before_refresh = self.main_page.find(MainPageLocators.PYTHON_FACT_LOCATOR, 5).text
            self.main_page.click(locator)
            python_fact_after_refresh = self.main_page.find(MainPageLocators.PYTHON_FACT_LOCATOR, 5).text
        with allure.step('Assert'):
            self.logger.info("End")
            assert python_fact_before_refresh != python_fact_after_refresh
