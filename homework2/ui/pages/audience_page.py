from ui.pages.base_page import BasePage
from ui.locators.locators import AudiencePageLocators, BasePageLocators
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from ui.pages.login_page import random_string


class AudiencePage(BasePage):
    locators = AudiencePageLocators

    def create_segment(self, login):
        self.click(BasePageLocators.AUDIENCE_LOCATOR)
        try:
            self.click(AudiencePageLocators.NEW_CREATE_LOCATOR)
        except TimeoutException:
            self.click(AudiencePageLocators.CREATE_BUTTON_LOCATOR)
        finally:
            self.click(AudiencePageLocators.SEGM_LOCATOR)
            self.click(AudiencePageLocators.CHECK_LOCATOR)
            self.click(AudiencePageLocators.ADD_SEGM_MODAL_LOCATOR)
            name_of_segment = random_string(10)
            self.input(AudiencePageLocators.NAME_OF_SEGM_LOCATOR, name_of_segment)
            self.click(AudiencePageLocators.CREATE_SEGM_LOCATOR)
            elem = self.find(AudiencePageLocators.CREATED_SEGMENT_LOCATOR)
            title_of_segment = elem.get_attribute("title")
            return (title_of_segment, name_of_segment)

    def elem_is_invisible(self, element,  timeout=None):
        return self.wait(timeout).until(EC.invisibility_of_element(element))

    def delete_segment(self):
        elem = self.find(AudiencePageLocators.CREATED_SEGMENT_LOCATOR)
        title_of_segment = elem.get_attribute("title")
        self.click(AudiencePageLocators.DELETE_SEGMENT_LOCATOR)
        self.click(AudiencePageLocators.CONFIRM_DELETE_LOCATOR)
        self.elem_is_invisible(elem, 30)
        return title_of_segment
