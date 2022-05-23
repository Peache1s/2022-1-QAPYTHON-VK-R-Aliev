from urllib.parse import urljoin
import requests
from requests.cookies import cookiejar_from_dict
from ui_tests.ui.pages.login_page import random_string


class ApiClient:

    def __init__(self, base_url, login, password):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.session = requests.Session()

    def _request(self, method, location, headers=None, data=None,json=None, params = None):
        url = urljoin(self.base_url, location)
        response = self.session.request(method=method, url=url, headers=headers, data=data, params=params, json=json)
        return response

    def post_login(self, login=None, password = None, session_flag=True):
        if login == None and password == None:
            login = self.login
            password = self.password
        data = {
            'username': login,
            'password': password,
            'submit': 'Login'
        }
        resp = self._request('POST', '/login', data=data)
        if session_flag:
            session = resp.history[0].headers['Set-Cookie'].split(';')[0].split('=')[1]
            self.session.cookies = cookiejar_from_dict({
                'session': session
            })
        return resp

    def post_registration(self, name, surname, username, email, password, confirm_password, middlename = '', checkbox = 'y', session_flag = True):
        data = {
            'name': name,
            'surname': surname,
            'middlename': middlename,
            'username': username,
            'email': email,
            'password': password,
            'confirm': confirm_password,
            'term': checkbox,
            'submit': 'Register'
        }
        resp = self._request('POST', '/reg', data = data)
        if session_flag:
            session = resp.history[0].headers['Set-Cookie'].split(';')[0].split('=')[1]
            self.session.cookies = cookiejar_from_dict({
                'session': session
            })
        return resp

    def get_logout(self):
        resp = self.session.request(url=self.base_url, method='GET')
        return resp

    def get_welcome(self):
        resp = self._request(method='GET', location='welcome/')
        return resp

    def add_user(self,name,surname, username,email,password, middlename = '' ,login = None, password_for_login = None ):
        self.post_login(login, password_for_login)
        headers = {'Content-Type': 'application/json'}
        data = {
            "name": name,
            "surname": surname,
            "middle_name": middlename,
            "username": username,
            "password": password,
            "email": email
        }
        location = 'api/user'
        response = self._request(method='POST', json = data, headers=headers, location=location )
        return response.status_code

    def delete_user(self, username, login = None, password_for_login = None):
        location = f'api/user/{username}'
        self.post_login(login, password_for_login)
        response = self._request(method='DELETE', location = location)
        return response.status_code

    def change_password(self, username_create = None, password = None, new_password = None, username_check = None, delete_flag = True):
        if username_create == None and password == None and new_password == None:
            username_create = random_string(10)
            password = random_string(4)
            new_password = random_string(4)
        if username_check == None:
            username_check = username_create
        self.add_user(name = random_string(10), surname= random_string(10), middlename= random_string(10), username=username_create, email = random_string(6)+'@mail.ru', password=password)
        headers = {'Content-Type': 'application/json'}
        data = {
                "password": f'{new_password}'
            }
        location = f'api/user/{username_check}/change-password'
        response = self._request(method='PUT', location=location, json=data, headers=headers)
        if delete_flag:
            self.delete_user(username_create)
            if username_check!= username_create:
                self.delete_user(username_check)
        return response.status_code

    def block_user(self, username = None, delete_flag = True, create_flag = True):
        if username == None:
            username = random_string(10)
        if create_flag:
            self.add_user(name=random_string(10), surname=random_string(10), middlename=random_string(10),
                                    username=username,
                                    email=random_string(4) + 'mail.ru', password=random_string(4))
        else:
            another_username = random_string(10)
            self.add_user(name=random_string(10), surname=random_string(10), middlename=random_string(10),
                                    username=another_username,
                                    email=random_string(4) + 'mail.ru', password=random_string(4))

        location = f'api/user/{username}/block'
        response = self._request(method='POST',location= location)
        if delete_flag:
            self.delete_user(username)
        return response.status_code

    def unblock_user(self, username, create_flag = False, delete_flag = True):
        if create_flag:
            another_username = random_string(10)
            self.add_user(name=random_string(10), surname=random_string(10), middlename=random_string(10),
                                    username=another_username,
                                    email=random_string(4) + 'mail.ru', password=random_string(4))
        location = f'api/user/{username}/accept'
        response = self._request(method='POST', location=location)
        if delete_flag:
            self.delete_user(username)
        return response.status_code
