import allure

from mysql.mysql_client import MysqlClient
from ui_tests.ui.pages.login_page import random_string
import pytest

@pytest.mark.api_login
@allure.feature("Api Login")
class TestApiLogin:

    @pytest.fixture(scope='function', autouse=True)
    def setup_mysql(self, mysql_client):
        self.mysql: MysqlClient = mysql_client

    @allure.description("""
    Проверка формы /login
    Проверяется наличие пользователя в бд,статус-код и значение set-cookie
    """)
    def test_valid_login(self, api_client):
        with allure.step("Response login"):
            response = api_client.post_login()
        with allure.step("Commit and Assert"):
            self.mysql.session.commit()
            assert self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.active == 1).filter(self.mysql.TestUsers.username == 'Peache1s').count() == 1
            assert 'Set-Cookie' not in response.headers
            assert response.status_code == 200

    @allure.description("""
    Проверка формы /login c с невалидными данными ( рандомными) 
    Проверяется наличие пользователя в бд,статус-код и значение set-cookie
    """)
    def test_invalid_login(self, api_client):
        username = random_string(10)
        with allure.step("Response login"):
            response = api_client.post_login(username, random_string(10), session_flag=False)
        with allure.step("Commit and Assert"):
            self.mysql.session.commit()
            assert self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.active == 1).filter(self.mysql.TestUsers.username == username).count() == 0
            assert 'Set-Cookie' in response.headers
            assert response.status_code == 401

    @allure.description("""
    Параметризированный тест формы /login c с невалидными данными: 
    -пустой username
    -пустой password
    -username меньше 6 символов
    Проверяется наличие пользователя в бд,статус-код и значение set-cookie
    """)
    @pytest.mark.parametrize("username, password", [
        ('', 10),
        (10, ''),
        (5, 10)
        ], indirect=['username', 'password'])
    def test_validation_errors(self, api_client, username, password):
        with allure.step("Response"):
            response = api_client.post_login(username, password, session_flag=False)
        with allure.step("Commit and Assert"):
            self.mysql.session.commit()
            assert self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.active == 1).filter(self.mysql.TestUsers.username == username).count() == 0
            assert 'Set-Cookie' in response.headers
            assert response.status_code == 401

@pytest.mark.api_registration
@allure.feature("Api Registration")
class TestApiRegistration:

    password = 'sometestpass'

    @pytest.fixture(scope='function', autouse=True)
    def setup_mysql(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
    @allure.description("""
    Тест на регистрацию пользователя с рандомным паролем и username( подходят под валидацию).
    Проверка статус-кода, значения set-cookie и отсуствия пользователя в бд до добавления и наличие после
    """)
    def test_registration(self, api_client):
        with allure.step("Response"):
            password = random_string(4)
            username = random_string(10)
            number_before_add = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.username == username).count()
            response = api_client.post_registration(name = random_string(10), surname= random_string(10),
                                                    middlename = random_string(10), username=username,
                                                    email = random_string(4)+'@mail.ru', password=password, confirm_password=password)
        with allure.step("Commit and Assert"):
            self.mysql.session.commit()
            number_after_add = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.username == username).count()
            assert (number_before_add == 0 and number_after_add == 1)
            assert 'Set-Cookie' not in response.headers
            assert response.status_code == 200

    @allure.description("""
    Тест на регистрацию пользователя с существующей почтой
    Проверка статус кода, того, что существует лишь один пользователь с указанными email в бд 
    """)
    def test_registration_with_existsing_email(self, api_client):
        with allure.step("Response"):
            email = random_string(5)+'@mail.ru'
            password = random_string(4)
            api_client.post_registration(name=random_string(10), surname=random_string(10),
                                           middlename=random_string(10), username=random_string(10),
                                           email=email, password=password, confirm_password=password)
            response = api_client.post_registration(name=random_string(10), surname=random_string(10),
                                                    middlename=random_string(10), username=random_string(10),
                                                    email=email, password=password,
                                                    confirm_password=password, session_flag=False)
        with allure.step("Commit and Assert"):
            self.mysql.session.commit()
            number_of_emails = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.email == email).count()
            assert number_of_emails == 1
            assert response.status_code == 304
            assert 'Set-Cookie' in response.headers


    @allure.description("""
    Параметризованный тест на валидацию входных данных:
    - много тестов на неправильный формат почты
    - тест на несовпадающие пароль и подтверждение пароля
    - тест на длину почты( короче 6 символов)
    - тест на пустые значения паролей
    - тест на пустое значение почты
    Проверка статус-кода и числа пользователей с указанной почтой
    """)
    @pytest.mark.parametrize("email, password, confirm_password, expected_code", [
        (7, password, password, 400),
        ('@', password, password, 400),
        ('@str', password, password, 400),
        ('.', password, password, 400),
        ('full', '111', '112', 400),
        (4, '111', '112', 400),
        ('full', '', '', 400),
        ('', password, password, 400)
        ], indirect=['email'])
    def test_negative_email_and_password(self, api_client, email, password, confirm_password, expected_code):
        with allure.step("Response"):
            response = api_client.post_registration(name=random_string(10), surname=random_string(10),
                                                    middlename=random_string(10), username=random_string(10),
                                                    email=email, password=password,
                                                    confirm_password=confirm_password, session_flag=False)
        with allure.step("Commit and Assert"):
            self.mysql.session.commit()
            number_of_emails = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.email == email).count()
            assert number_of_emails == 0
            assert response.status_code == expected_code
            assert 'Set-Cookie' in response.headers

    @allure.description("""
    Тест регистрации пользователя с существующим именем
    Cначала создается пользователя с рандомным username, после - проверяется регистрация пользователя с таким же именем.
    Проверка наличия в бд лишь одного польщователя с указанным username, статус-кода и set-cookies
    
    """)
    def test_registration_with_existing_user(self, api_client):
        with allure.step("Create new user:"):

            username = random_string(10)

            api_client.post_registration(name=random_string(10), surname=random_string(10),
                                           middlename=random_string(10), username=username,
                                           email=random_string(5)+'@mail.ru', password='0000', confirm_password='0000')
        with allure.step("Add user with existing username"):
            response = api_client.post_registration(name=random_string(10), surname=random_string(10),
                                           middlename = random_string(10), username=username,
                                           email = random_string(5)+'@mail.ru', password='0000', confirm_password='0000', session_flag=False)
        with allure.step("Commit and assert"):
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.username == username).count()
            assert number_of_users == 1
            assert response.status_code == 304
            assert 'Set-Cookie' in response.headers

    @allure.description("""
    Параметризированный тест на валидацию в форме регистрации:
    -отсутствие name
    -отсутствие surname
    -короткий username
    -невалидный email
    Проверка отсутствие username в бд, статус-кода и set-cookies
    """)
    @pytest.mark.parametrize(
        "name, surname, middlename, username, email, password, expected_code", [
            ('', 7, 7, 7, 'full', 7,400),
            (7, '', 7, 7, 'full', 7, 400),
            (7, 7, 7, 5, 'full', 7, 400),
            (7, 7, 7, 7, 5, 7, 400)
        ], indirect=['name', 'surname', 'middlename', 'username', 'email','password'])
    def test_negative_validation_registration(self,api_client, name, surname, middlename, username, email, password, expected_code):
        with allure.step("Response"):
            response = api_client.post_registration(name=name, surname=surname,
                                           middlename=middlename, username=username,
                                           email=email, password=password, confirm_password=password, session_flag=False)
        self.mysql.session.commit()
        with allure.step("Commit and assert"):
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.username == username).count()
            assert number_of_users == 0
            assert response.status_code == expected_code
            assert 'Set-Cookie' in response.headers
    @allure.description("""
    Прохождение на location = welcome/ ( сразу на страницу) без предварительной авторизации
    Проверка статус-кода
    """)
    def test_welcome_without_authorization(self, api_client):
        with allure.step("Response"):
            response = api_client.get_welcome()
        with allure.step("Assert"):
            return response.status_code == 302


@pytest.mark.api_general
@allure.feature('Api general')
class TestApiGeneral:

    @pytest.fixture(scope = 'function', autouse = True)
    def setup_mysql(self, mysql_client):
        self.mysql: MysqlClient = mysql_client

    @allure.description("""
    Тест на добавление пользователя через api (  с рандомными данными ) 
    Проверка наличия его в бд и статус-кода
    """)
    def test_add_user(self, api_client):
        with allure.step("Response"):
            username = random_string(10)
            status_code = api_client.add_user(name = random_string(10), surname= random_string(10), middlename= random_string(10), username=username,
                        email = random_string(4)+'mail.ru', password=random_string(4))
        with allure.step("Commit and assert"):
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.username == username).count()
            assert number_of_users == 1
            api_client.delete_user(username)
            assert status_code == 201

    @allure.description("""
    Тест на добавление пользователя с существующим username
    Проверка статус-кода и наличия лишь 1 пользователя в бд
    """)
    def test_add_existing(self, api_client):
        with allure.step("Add new user"):
            username = random_string(10)
            api_client.add_user(name = random_string(10), surname= random_string(10), middlename= random_string(10), username=username,
                        email = random_string(4)+'mail.ru', password=random_string(4))
        with allure.step("Add user with existing username"):
            status_code = api_client.add_user(name = random_string(10), surname= random_string(10), middlename= random_string(10), username=username,
                        email = random_string(4)+'mail.ru', password=random_string(4))
        with allure.step("Commit and assert"):
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(
                self.mysql.TestUsers.username == username).count()
            assert number_of_users == 1
            api_client.delete_user(username)
            return status_code == 304


    @allure.description("""
    Тест на добавление пользователя с существующей почтой.
    Создается новый пользователь с рандомной почтой. 
    Эта же почта используется при создании другого пользователя.
    Проверка статус-кода и наличия лишь 1 пользователя с указанной почтой в бд
    """)
    def test_add_existing_email(self, api_client):
        with allure.step("Add new user:"):
            email = random_string(10)+'@mail.ru'
            username1 = random_string(10)
            username2 = random_string(10)
            api_client.add_user(name = random_string(10), surname= random_string(10), middlename= random_string(10), username=username1,
                        email = email, password=random_string(4))
        with allure.step("Add user with existing email"):
            status_code = api_client.add_user(name = random_string(10), surname= random_string(10), middlename= random_string(10), username=username2,
                        email = email, password=random_string(4))
        with allure.step("Commit and assert"):
            self.mysql.session.commit()
            number_of_email = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.email == email).count()
            assert number_of_email == 1
            api_client.delete_user(username1)
            return status_code == 304

    @allure.description("""
    Тест на валидацию добавления пользователя через api:
    -тест на пустой name 
    -тест на пустой surname
    -тест на пустой username
    -много тестов на невалидный email
    -тест на короткий email
    -тесты на  длину поля ( превышение количества символов )
    """)
    @pytest.mark.parametrize("name, surname, middlename, username, email, password, expected_code", [
    ('', 10, 10, 10, 'full', 7, 400),
    (10, '', 10, 10, 'full', 7, 400),
    (10, 10, 10, '', 'full', 7, 400),
    (10, 10, 10, 4, 'full', 7, 400),
    (10, 10, 10, 10, '', 7, 400),
    (10, 10, 10, 10, 5, 7, 400),
    (10, 10, 10, 10, 6, 7, 400),
    (10, 10, 10, 10, '@str', 7, 400),
    (10, 10, 10, 10, '.', 7, 400),
    (10, 10, 10, 10, 'full', '', 400),
    (256, 10, 10, 10, 'full', 7, 400),
    (10, 256, 10, 10, 'full', 7, 400),
    (10, 10, 256, 10, 'full', 7, 400),
    (10, 10, 10, 17, 'full', 7, 400),
    (256, 10, 10, 10, 65, 256, 400)
    ], indirect=['name', 'surname', 'middlename','username', 'email', 'password'])
    def test_validation_add_user(self, api_client, name, surname, middlename, username, email, password, expected_code):
        with allure.step("Add user"):
            status_code = api_client.add_user(name = name, surname= surname, middlename= middlename, username=username,
                        email = email, password=password)
        with allure.step("Commit and assert"):
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(
                self.mysql.TestUsers.username == username).count()
            assert number_of_users == 1
            api_client.delete_user(username)
            assert status_code == expected_code

    @pytest.mark.ll
    @allure.description("""
    Тест на удаление пользователя.
    Проверка наличия пользователя до удаления и после ( пользователь создается в тесте )
    Проверяется статус-код и наличие/отсутствие пользователя до и после теста
    """)
    def test_delete(self, api_client):
        with allure.step("Add and delete user"):
            username = random_string(10)
            number_of_users_before = self.mysql.session.query(self.mysql.TestUsers).filter(self.mysql.TestUsers.username == username).count()
            api_client.add_user(name = random_string(10), surname= random_string(10), middlename= random_string(10), username=username,
                        email = random_string(4)+'mail.ru', password=random_string(4))
        with allure.step("Commit and assert"):
            self.mysql.session.commit()
            number_of_users_after = self.mysql.session.query(self.mysql.TestUsers).filter(
                self.mysql.TestUsers.username == username).count()
            assert (number_of_users_before == 0 and number_of_users_after ==1)
            status_code = api_client.delete_user(username)
            assert status_code == 204

    @allure.description("""
    Тест на удаление существующего пользователя
    Проверка статус кода
    """)
    def test_delete_not_existing(self, api_client):
        with allure.step("Response"):
            username = random_string(10)
            status_code = api_client.delete_user(username)
        with allure.step("Assert"):
            assert status_code == 404

    @allure.description("""
    Тест на смену пароля пользователя.
    Создается новый пользователь, после чего у него изменяется пароль.
    Проверка наличия в бд этого пользователя с новым паролем и статус-кода
    """)
    def test_change_password(self, api_client):
        with allure.step("Add user and change password"):
            username = random_string(10)
            password_old = random_string(6)
            password_new = random_string(6)
            status_code = api_client.change_password(password=password_old, new_password=password_new, username_create=username, delete_flag=False)
        with allure.step('Commit and assert'):
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(
                self.mysql.TestUsers.username == username and self.mysql.TestUsers.password == password_new).count()
            assert number_of_users == 1
            api_client.delete_user(username)
            assert status_code == 200

    @allure.description("""
    Тест на смену пароля несуществующему пользователю.
    Проверка статус-кода
    """)
    def test_change_not_existing_password(self, api_client):
        with allure.step("Add user and change password"):
            status_code = api_client.change_password(username_create=random_string(10), password=random_string(10), new_password=random_string(10), username_check=random_string(10))
        with allure.step('Assert'):
            assert status_code == 404

    @allure.description("""
    Тест на блокировку пользователя.
    Создается новый пользователь, после чего он блокируется. 
    Проверяется access статус в бд и статус-код""")
    def test_block_user(self, api_client):
        with allure.step('Add and block'):
            username = random_string(10)
            status_code = api_client.block_user(username= username, delete_flag=False)
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(
                self.mysql.TestUsers.username == username and self.mysql.TestUsers.access == 0 ).count()
        with allure.step("delete user"):
            api_client.delete_user(username)
        with allure.step("Assert"):
            assert number_of_users == 1
            assert status_code == 200

    @allure.description("""
    Тест на блокировку несуществующего пользователя, 
    создается новый пользователь для авторизации. С его поомщью блокируется другой. 
    Проверка статус-кода.
    """)
    def test_block_not_existing_user(self, api_client):
        with allure.step("Add and block"):
            username = random_string(10)
            status_code = api_client.block_user(username, create_flag=False)
        with allure.step('Assert'):
            assert status_code == 404

    @allure.description("""
    Тест на разблокировку пользователя.
    Создается пользователь и блокируется. После чего происходит его разблокировка.
    Проверка статус-кода и наличия/отсуствия до/после разблокировки access = 0/1
    """)

    def test_unblock_user(self, api_client):
        with allure.step("Add and block"):
            username = random_string(10)
            block_status_code = api_client.block_user(username, delete_flag=False)
            assert block_status_code == 200
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(
                self.mysql.TestUsers.username == username and self.mysql.TestUsers.access == 0 ).count()
            assert number_of_users == 1
        with allure.step("unblock"):
            unblock_status_code = api_client.unblock_user(username)
            assert unblock_status_code == 200
        with allure.step('Commit and assert'):
            self.mysql.session.commit()
            number_of_users = self.mysql.session.query(self.mysql.TestUsers).filter(
                self.mysql.TestUsers.username == username and self.mysql.TestUsers.access == 1 ).count()
            assert number_of_users == 0

    @allure.description("""
    Тест на разблокировку несуществующего пользователя
    Проверка статус-кода""")
    def test_unblock_not_existing_user(self, api_client):
        with allure.step("Unblock"):
            username = random_string(10)
            status_code = api_client.unblock_user(username, create_flag=True)
        with allure.step('Assert'):
            assert status_code == 404
