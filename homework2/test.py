import allure
import pytest
from selenium.common.exceptions import TimeoutException
from base import BaseCase
from ui.locators.locators import LoginPageLocators, AudiencePageLocators
from ui.pages.login_page import random_string, random_number


class TestOne(BaseCase):

    @pytest.mark.UI
    @allure.description("""
    Логинится с логином из цифр, симулирующим ввод неверного номера телефона.
    Проверка выплывающей ошибки на новой странице"
    """)
    @allure.feature("Log in")
    @allure.story("Log in with wrong number")
    def test_negative_number_log_in(self):
        with allure.step("Log in"):
            self.logger.info("Start")
            self.login_page.login(random_number(11), random_string(10))
            elem = self.login_page.find(LoginPageLocators.LOG_IN_ERR_NUMBER_LOCATOR, 20)
        with allure.step("Assert"):
            try:
                self.login_page.elem_is_visible(elem, 20)
                self.logger.info("End")
                assert True
            except TimeoutException:
                self.logger.info("End")
                assert False

    @pytest.mark.UI
    @allure.description("""
    Логинится с логином из символов, симулирующим ввод неверного email.
    Проверка всплывающего окна 
    """)
    @allure.feature("Log in")
    @allure.story("Log in with wrong email")
    def test_negative_email_log_in(self):
        self.logger.info("Start")
        with allure.step("Log in"):
            self.login_page.login(random_string(11), random_string(10))
        with allure.step("Assert"):
            try:
                self.login_page.find(LoginPageLocators.LOG_IN_ERR_LOCATOR)
                self.logger.info("End")
                assert True
            except TimeoutException:
                self.logger.info("End")
                assert False

    @pytest.mark.UI
    @allure.description("""
    Создание сегмента и проверка сравнением задаваемого имени сегмента с именем последнего сегмента
    """)
    @allure.feature("Segment")
    def test_create_segment(self, login):
        self.logger.info("Start")
        with allure.step("Create Segment"):
            answer = self.audience_page.create_segment(login)
            title_of_segment = answer[0]
            name_of_segment = answer[1]
        with allure.step("Assert"):
            self.logger.info("End")
            assert title_of_segment == name_of_segment
            answer = self.audience_page.delete_segment()
            elem = self.audience_page.find(AudiencePageLocators.CREATED_SEGMENT_LOCATOR)
            new_title_segment = elem.get_attribute("title")
            assert answer != new_title_segment


    @pytest.mark.UI
    @allure.description("""
       Создает новый сегмент и сравнивает его имя с последним созданным сегментом после удаления
       """)
    @allure.feature("Segment")
    def test_delete_segment(self, login):
        self.logger.info("Start")
        with allure.step("Create Segment"):
            answer = self.audience_page.create_segment(login)
            title_of_created_segment = answer[0]
            name_of_created_segment = answer[1]
            assert title_of_created_segment == name_of_created_segment
        with allure.step("Compare the name of the last created segment before deletion and after"):
            title_of_segment = self.audience_page.delete_segment()
            elem = self.audience_page.find(AudiencePageLocators.CREATED_SEGMENT_LOCATOR)
        with allure.step("Assert"):
            new_title_segment = elem.get_attribute("title")
            self.logger.info("End")
            assert title_of_segment != new_title_segment


    @pytest.mark.UI
    @allure.description("""
    Тест для создания кампании: 
    Создается самая простая компания trafic, далее генерируется случайное имя кампании,
    а также из РАБОЧЕГО СТОЛА загружается файл для баннера с названием FROG.jpeg
    """)
    @allure.feature("Campaign")
    def test_create_campaign(self, login):
        self.logger.info("Start")
        answer = self.campaign_page.create_campaign()
        self.logger.info("End")
        assert answer[0] == answer[1]