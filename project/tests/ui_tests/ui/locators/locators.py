from selenium.webdriver.common.by import By


class BasePageLocators:
    pass

class LoginPageLocators:
    LOG_IN_LOCATOR = (By.ID, "username")
    PASSWORD_LOCATOR = (By.ID, "password")
    SUBMIT_LOCATOR = (By.ID, "submit")
    ERROR_LOG_IN_LOCATOR = (By.ID, "flash")
    REGISTRATION_LOCATOR = (By.XPATH, "//div[contains(@class,'uk-text-small')]/a")


class RegistrationPageLocators:
    NAME_LOCATOR = (By.NAME, "name")
    SURNAME_LOCATOR = (By.NAME,"surname")
    MIDDLENAME_LOCATOR = (By.NAME, "middlename")
    USERNAME_LOCATOR = (By.NAME, "username")
    EMAIL_LOCATOR = (By.NAME, 'email')
    PASSWORD_LOCATOR = (By.NAME, 'password')
    CONFIRM_PASSWORD_LOCATOR = (By.NAME, "confirm")
    REGISTRATION_BUTTON_LOCATOR = (By.ID, "submit")
    REGISTRATION_ACCEPT = (By.ID, "term")
    ERROR_LOCATOR = (By.ID, "flash")


class MainPageLocators:

    LOG_OUT_LOCATOR = (By.ID, "logout")
    PYTHON_LOCATOR = (By.XPATH, '//nav[@class="uk-navbar"]/ul/li[2]/a')
    PYTHON_CHECK = (By.CLASS_NAME, 'python-logo')
    PYTHON_LIST_LOCATOR = (By.XPATH, '//nav[@class="uk-navbar"]/ul/li[2]')
    API_LOCATOR = (By.XPATH, '//div[2]/div[1]/figure/a/img')
    FUTURE_LOCATOR = (By.XPATH, '//div[2]/div[2]/figure/a/img')
    SMTP_LOCATOR = (By.XPATH, '//div[2]/div[3]/figure/a/img')
    HISTORY_OF_PYTHON_LOCATOR = (By.XPATH, '//ul[contains(@class,"uk-nav-navbar")]/li[1]/a')
    ABOUT_FLASK_LOCATOR = (By.XPATH, '//ul[contains(@class,"uk-nav-navbar")]/li[2]/a')
    LINUX_LOCATOR = (By.XPATH, '//nav[@class="uk-navbar"]/ul/li[3]')
    CENTOS_LOCATOR = (By.XPATH, '//li[3]/div/ul/li/a')
    NETWORK_LOCATOR = (By.XPATH, '//nav[@class="uk-navbar"]/ul/li[4]')
    WIRESHARK_NEWS_LOCATOR = (By.XPATH, '//ul[@class = "uk-nav-sub"]/li[1]/a')
    WIRESHARK_DOWNLOAD_LOCATOR = (By.XPATH, '//ul[@class = "uk-nav-sub"]/li[2]/a')
    TCPDUMP_EXAMPLES_LOCATOR = (By.XPATH, '//li[@class = "uk-nav-header"][2]/ul/li/a')
    PYTHON_FACT_LOCATOR = (By.XPATH, '//div[contains(@class, "uk-text-large")]/p')
    HOME_LOCATOR = (By.XPATH, '//nav[@class="uk-navbar"]/ul/li[1]')
    BUG_PICTURE_LOCATOR = (By.XPATH, '//nav[@class="uk-navbar"]/ul/a')