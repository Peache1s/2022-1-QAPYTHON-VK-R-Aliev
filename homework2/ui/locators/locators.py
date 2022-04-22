from selenium.webdriver.common.by import By


class BasePageLocators:
    AUDIENCE_LOCATOR = (By.XPATH, '//a[contains(@class,"center-module-segments")]')
    CAMPAIGN_LOCATOR = (By.XPATH, '//a[contains(@class,"center-module-campaigns")]')


class LoginPageLocators:
    LOG_IN_LOCATOR = (By.XPATH, '//div[contains(@class,"responseHead-module-button")]')
    NAME_LOCATOR = (By.NAME, "email")
    PASSW_LOCATOR = (By.NAME, "password")
    LOG_IN_ERR_LOCATOR = (By.XPATH, '//div[contains(@class, "notify-module-content")]')
    LOG_IN_ERR_NUMBER_LOCATOR = (By.XPATH, '//div[text()="Invalid login or password"]')


class AudiencePageLocators:
    CHECK_LOCATOR = (By.XPATH, '//input[contains(@class, "adding-segments-source__checkbox")]')
    CREATE_BUTTON_LOCATOR = (By.XPATH, "//button[@class='button button_submit']")
    NEW_CREATE_LOCATOR = (By.LINK_TEXT, "Create")
    SEGM_LOCATOR = (By.XPATH, '//div[@class = "adding-segments-item"]')
    ADD_SEGM_MODAL_LOCATOR = (By.XPATH, '//div[@class = "adding-segments-modal__btn-wrap js-add-button"]/button')
    CREATE_SEGM_LOCATOR = (By.XPATH, '//div[contains(@class,"js-create-segment-button-wrap")]/button')
    NAME_OF_SEGM_LOCATOR = (By.XPATH, '//div[@class = "js-segment-name"]/div/div/input')
    CREATED_SEGMENT_LOCATOR = (By.XPATH, '//div[contains(@class, "cells-module-nameCell")]/a')
    DELETE_SEGMENT_LOCATOR = (By.XPATH, '//span[contains(@class, "icon-cross cells-module-removeCell")]')
    CONFIRM_DELETE_LOCATOR = (By.XPATH, '//button[@class = "button button_confirm-remove button_general"]')


class CampaignPageLocators:
    CREATE_CAMPAIGN_LOCATOR = (By.XPATH, '//div[contains(@class, "button-module-blue")]')
    TRAFFIC_LOCATOR = (By.XPATH, '//div[@class = "column-list-item _traffic"]')
    INPUT_LINK_LOCATOR = (By.XPATH, '//div[contains(@class, "mainUrl-module-inputWrap")]/div/div/input')
    NAME_OF_CAMPAIGN = (By.XPATH, '//div[contains(@class, "input_campaign-name")]/div[2]/input')
    BANNER_LOCATOR = (By.ID, 'patterns_banner_4')
    ADD_PICTURE_LOCATOR = (By.XPATH,'//div[contains(@class, "upload-module-wrapper")][1]/input')
    ADD_PICTURE_LOCATOR_SMALL = (By.XPATH, '//div[contains(@class, "roles-module-buttonWrap")]/div[2]/input')
    ELEM_SUBMIT_SMALL = (By.XPATH, '//input[contains(@class, "image-cropper__save")]')
    FINAL_CREATE_CAMPAIGN = (By.XPATH, '//div[@class = "footer__button js-save-button-wrap"]/button')
    NAME_OF_CREATED_CAMPAIGN = (By.XPATH, '//a[contains(@class, "nameCell-module-campaignNameLink")]')
