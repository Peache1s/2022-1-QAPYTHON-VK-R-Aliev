import allure
from ui.pages.base_page import BasePage
from ui.locators.locators import CampaignPageLocators
import ui.pages.login_page as lp


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
            name_web = self.find(CampaignPageLocators.NAME_OF_CREATED_CAMPAIGN, 20)
            visible_name_of_campaign = name_web.get_attribute("title")
            return (name_of_campaign, visible_name_of_campaign)
