import time
import logging
from typing import NoReturn
from .base_page import BasePage
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class VirginMediaPage(BasePage):
    def __init__(self, api_key: str, login: str, password: str):
        super(VirginMediaPage, self).__init__(api_key, login, password)

    _auth_page = "https://www.virginmedia.com/my-virgin-media"

    # XPATH locators
    _login_input_locator = "//input[@id='identifierInput']"
    _password_input_locator = "//input[@id='password']"
    _login_form_locator = "//vm-button[@data-cy='sign-in-button']"
    _login_continue_locator = "//div[@id='postButton']"
    _accept_cookies_locator = "//*[@id='onetrust-accept-btn-handler']"
    _captcha_iframe = "//div[@id='recaptcha']"
    _latest_bill_button_locator = "//vm-button[@data-cy='view-bill-paid-pending']"
    _close_bill_explainer_locator = "//button[starts-with(@class, 'tour-tooltip-header__close')]"
    _download_pdf_button_locator = "//vm-button[@data-cy='downloadPDFBtn']//button"
    _is_credentials_is_correct_locator = "//*[contains(text(), ' Your email or password was incorrect')]"

    @property
    def login_continue_button(self) -> WebElement:
        return self._get_element(self._login_continue_locator)

    @property
    def latest_bill_button(self) -> WebElement:
        return self._get_element(self._latest_bill_button_locator)

    @property
    def _capthca_site_key(self) -> str:
        return self._get_element(self._captcha_iframe).get_attribute('data-sitekey')

    @property
    def close_bill_explainer_button(self) -> WebElement:
        return self._get_element(self._close_bill_explainer_locator)

    @property
    def donwload_pdf_button(self) -> WebElement:
        return self._get_element(self._download_pdf_button_locator)

    @property
    def is_credentials_is_correct_element(self) -> WebElement:
        return self._get_element(self._is_credentials_is_correct_locator)

    def _is_credentials_is_correct(self) -> bool:
        try:
            self.is_credentials_is_correct_element
            return False
        except Exception:
            return True

    def _accept_cookies_policy(self):
        try:
            logging.info(f"Trying to accept cookies")
            if self._accept_cookies_locator != '':
                self._accept_cookies_button.click()
                time.sleep(1)
            logging.info(f"Cookies policy accepted")
        except Exception:
            logging.info(f"No cookies policy")

    def _close_bill_explainer(self):
        try:
            self.close_bill_explainer_button.click()
        except Exception:
            pass

    def _solve_captcha(self):
        logging.info(f"Solving captcha: {str(self._capthca_site_key)}")
        code = self._captcha_solver.recaptcha(sitekey=self._capthca_site_key, url=self._driver.current_url, invisible=1)['code']
        logging.info(f"Captcha was solved {code}")
        self._driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{code}"; submitForm();')

    def do_authorisation(self):
        self.login_form_button.click()
        logging.info(f"Input login: {self._login}")
        self.login_input = self._login
        logging.info(f"Login confirmed")
        self.login_continue_button.click()
        self.password_input = self._password
        logging.info(f"Password confirmed")
        self._solve_captcha()
        logging.info(f"Captcha was solved")

    def run(self):
        self.do_authorisation()
        logging.info(f"Opening latest bill page")
        self.latest_bill_button.click()
        logging.info(f"Closing bill exaplainer")
        self._close_bill_explainer()
        logging.info(f"Downloading latest bill")

        wait = WebDriverWait(self._driver, 10)  # wait up to 10 seconds
        element = wait.until(EC.element_to_be_clickable((By.XPATH, self._download_pdf_button_locator)))

        self.donwload_pdf_button.click()
        time.sleep(10)