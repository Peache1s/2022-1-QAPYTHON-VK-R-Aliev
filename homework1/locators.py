from selenium.webdriver.common.by import By

LOG_IN_LOCATOR = (By.XPATH, '//div[contains(@class,"responseHead-module-button")]')
NAME_LOCATOR = (By.NAME, "email")
PASSW_LOCATOR = (By.NAME, "password")
CONT_INFO_LOCATOR = (By.XPATH, '//a[contains(@class,"center-module-profile")]')
CONT_NAME_LOCATOR = (By.XPATH, '//input[@maxlength="100"]')
CONT_NUMB_LOCATOR = (By.XPATH, '//input[@maxlength="20"]')
CONT_SUBMIT_LOCATOR = (By.XPATH, "//button[@class='button button_submit']")
STAT_LOCATOR = (By.XPATH, '//a[contains(@class,"center-module-statistics")]')
BILLING_LOCATOR = (By.XPATH, '//a[contains(@class,"center-module-billing")]')
LOG_OUT_LOCATOR1 = (By.XPATH, '//div[contains(@class,"right-module-rightButton")]')
LOG_OUT_LOCATOR2 = (By.XPATH, '//li[2][contains(@class, "rightMenu-module-rightMenuItem")]')

