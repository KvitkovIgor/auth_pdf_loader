import time
import logging
from typing import NoReturn
from .base_page import BasePage
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs


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
    _captcha_iframe = "//iframe[starts-with(@src, 'https://www.google.com/recaptcha/api2/anchor')]"

    # check is credentials are correct
    def _is_credentials_is_correct(self) -> bool:
        try:
            self._get_element(self._is_credentials_is_correct_locator)
            return False
        except Exception:
            return True

    # accepting cookies
    def _accept_cookies_policy(self):
        try:
            logging.info(f"Trying to accept cookies")
            self._get_element(self._accept_cookies_locator).click()
            logging.info(f"Cookies policy accepted")
        except Exception:
            logging.info(f"No cookies policy")

    def _close_bill_explainer(self):
        try:
            self._get_element(self._close_bill_explainer_locator).click()
        except Exception:
            pass

    # solving captcha method
    def _solve_captcha(self):
        captcha_site_key = parse_qs(urlparse(self._get_element(self._captcha_iframe).get_attribute("src")).query)['k'][0]
        logging.info(f"Solving captcha: {str(captcha_site_key)}")
        code = self._captcha_solver.recaptcha(sitekey=captcha_site_key, url=self._driver.current_url, invisible=1)['code']
        logging.info(f"Captcha was solved {code}")
        self._driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{code}"; submitForm();')

    def run(self) -> NoReturn:
        # opening auth page
        self._driver.get(self._auth_page)
        logging.info(f"Opened auth page {self._auth_page}")

        # trying to accept cookies
        self._driver.implicitly_wait(30)
        self._accept_cookies_policy()
        logging.info("Cookies accepted")
        time.sleep(2)

        # doing authorisation
        wait = WebDriverWait(self._driver, 10)  # wait up to 10 seconds
        element = wait.until(EC.element_to_be_clickable((By.XPATH, self._login_form_locator)))
        self._get_element(self._login_form_locator).click()
        logging.info(f"Input login: {self._login}")
        self._get_element(self._login_input_locator).send_keys(self._login)
        logging.info(f"Login confirmed")

        # opening next page with password and captcha
        self._get_element(self._login_continue_locator).click()
        self._get_element(self._password_input_locator).send_keys(self._password)
        logging.info(f"Password confirmed")

        # solving captcha
        self._solve_captcha()
        logging.info(f"Captcha was solved")

        # check is input credenatials correct
        assert self._is_credentials_is_correct(), "Wrong credentials"

        logging.info(f"Opening latest bill page")
        self._get_element(self._latest_bill_button_locator).click()

        # need to close bill explainer if it appears
        logging.info(f"Closing bill exaplainer")
        self._close_bill_explainer()
        logging.info(f"Downloading latest bill")

        wait = WebDriverWait(self._driver, 10)  # wait up to 10 seconds
        element = wait.until(EC.element_to_be_clickable((By.XPATH, self._download_pdf_button_locator)))

        # add logic to get banners & popups out of the way.
        #click class="CRO-528--banner-close"
        #click class="QSIWebResponsiveDialog-Layout1-SI_ezf2xkiB7FZrb38_close-btn"

        time.sleep(2)
        self._get_element(self._download_pdf_button_locator).click()
        time.sleep(2)

