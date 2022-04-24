import allure
from selenium.webdriver.common.by import By
from ui.pages.base_page import BasePage
from ui.locators.locators import CampaignPageLocators
import ui.pages.login_page as lp
from datetime import datetime


class CampaignPage(BasePage):
    locators = CampaignPageLocators

    def create_campaign(self):
        with allure.step("Create the Campaign"):
            self.click(CampaignPageLocators.CREATE_CAMPAIGN_LOCATOR, 15)
            self.click(CampaignPageLocators.TRAFFIC_LOCATOR, 15)
            self.input(CampaignPageLocators.INPUT_LINK_LOCATOR, 'https://github.com/Peache1s', 15)
        with allure.step("Confirm campaign options"):
            self.find(CampaignPageLocators.NAME_OF_CAMPAIGN, 20)
            name_of_campaign = lp.random_string(10)
            self.click(CampaignPageLocators.NAME_OF_CAMPAIGN, 20)
            self.input(CampaignPageLocators.NAME_OF_CAMPAIGN, name_of_campaign, 20)
            self.click(CampaignPageLocators.BANNER_LOCATOR, 20)
            self.upload(CampaignPageLocators.ADD_PICTURE_LOCATOR, 20)
            self.upload(CampaignPageLocators.ADD_PICTURE_LOCATOR_SMALL, 20)
            self.click(CampaignPageLocators.ELEM_SUBMIT_SMALL, 20)
            self.click(CampaignPageLocators.FINAL_CREATE_CAMPAIGN, 20)
        with allure.step("Check and assert"):
            name = CampaignPageLocators.PROTOTYPE_NAME_OF_CREATED_CAMPAIGN + f'"{name_of_campaign}"]'
            NAME_OF_CREATED_CAMPAIGN = (By.XPATH, name)
            name_web = self.find(NAME_OF_CREATED_CAMPAIGN, 20)
            visible_name_of_campaign = name_web.get_attribute("title")
            return (name_of_campaign, visible_name_of_campaign, name_web)

    def delete_campaign(self, element ):
        with allure.step("Delete the Campaign"):
            par_element = element.find_element_by_xpath('..').find_element_by_xpath('..')
            row = par_element.get_attribute("data-row-id")
            string_for_locator = f'//div[@data-row-id = "{row}"]'+CampaignPageLocators.DELETE_SETTINGS
            DELETE_SETTINGS_LOCATOR = (By.XPATH, string_for_locator)
            self.click(DELETE_SETTINGS_LOCATOR)
            self.click(CampaignPageLocators.REMOVE_LOCATOR)
            check_string = f'//div[@data-row-id = "{row}"]'+CampaignPageLocators.CHECK_DELETE_PROTOTYPE
            CHECK_LOCATOR = (By.XPATH, check_string)
            del_string = self.find(CHECK_LOCATOR).text
            start_time = datetime.now()
            while del_string != 'Deleted campaign':
                del_string = self.find(CHECK_LOCATOR).text
                time_delta = datetime.now()-start_time
                if time_delta.total_seconds() >= 15:
                    break
            return del_string