import time
import logging
from typing import NoReturn
from .base_page import BasePage
from selenium.webdriver.remote.webelement import WebElement

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
    _download_pdf_button_locator = "//vm-button[@data-cy='downloadPDFBtn']"

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
        self.login_input = self._login
        self.login_continue_button.click()
        self.password_input = self._password
        self._solve_captcha()

    def run(self) -> NoReturn:
        self.do_authorisation()
        time.sleep(100)
        self.latest_bill_button.click()
        self._close_bill_explainer()
        self.donwload_pdf_button.click()
