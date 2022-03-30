import allure
import pytest
from selenium.common.exceptions import TimeoutException
from base import BaseCase
from ui.locators.locators import LoginPageLocators, AudiencePageLocators, CampaignPageLocators
from selenium.webdriver.common.keys import Keys
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
            self.login_page.click(LoginPageLocators.LOG_IN_LOCATOR)
            self.login_page.input(LoginPageLocators.NAME_LOCATOR, random_number(11))
            elem = self.login_page.input(LoginPageLocators.PASSW_LOCATOR, random_string(10))
            elem.send_keys(Keys.ENTER)
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
            self.login_page.click(LoginPageLocators.LOG_IN_LOCATOR)
            self.login_page.input(LoginPageLocators.NAME_LOCATOR, random_string(11))
            elem = self.login_page.input(LoginPageLocators.PASSW_LOCATOR, random_string(10))
            elem.send_keys(Keys.ENTER)
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

    @pytest.mark.UI
    @allure.description("""
    Создает новый сегмент и сравнивает его имя с последним созданным сегментом после удаления
    """)
    @allure.feature("Segment")
    def test_delete_segment(self, login):
        self.logger.info("Start")
        with allure.step("Create Segment"):
            answer = self.audience_page.create_segment(login)
        with allure.step("Compare the name of the last created segment before deletion and after"):
            elem = self.audience_page.find(AudiencePageLocators.CREATED_SEGMENT_LOCATOR)
            title_of_segment = elem.get_attribute("title")
            self.audience_page.click(AudiencePageLocators.DELETE_SEGMENT_LOCATOR)
            self.audience_page.click(AudiencePageLocators.CONFIRM_DELETE_LOCATOR)
            self.audience_page.elem_is_invisible(elem)
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
        elem = login
        with allure.step("Create the Campaign"):
            elem.click(CampaignPageLocators.CREATE_CAMPAIGN_LOCATOR,15)
            elem.click(CampaignPageLocators.TRAFFIC_LOCATOR, 15)
            elem.input(CampaignPageLocators.INPUT_LINK_LOCATOR, 'https://github.com/Peache1s', 15)
        with allure.step("Confirm campaign options"):
            elem.find(CampaignPageLocators.NAME_OF_CAMPAIGN, 20)
            name_of_campaign = random_string(10)
            elem.click(CampaignPageLocators.NAME_OF_CAMPAIGN, 20)
            elem.input(CampaignPageLocators.NAME_OF_CAMPAIGN, name_of_campaign, 20)
            elem.click(CampaignPageLocators.BANNER_LOCATOR, 20)
            elem.upload(CampaignPageLocators.ADD_PICTURE_LOCATOR, 20)
            elem.upload(CampaignPageLocators.ADD_PICTURE_LOCATOR_SMALL, 20)
            elem.click(CampaignPageLocators.ELEM_SUBMIT_SMALL, 20)
            elem.click(CampaignPageLocators.FINAL_CREATE_CAMPAIGN, 20)
        with allure.step("Check and assert"):
            name_web = elem.find(CampaignPageLocators.NAME_OF_CREATED_CAMPAIGN, 20)
            visible_name_of_campaign = name_web.get_attribute("title")
            self.logger.info("End")
            assert name_of_campaign == visible_name_of_campaign
