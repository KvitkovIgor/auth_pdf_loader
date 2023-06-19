import logging
import time
import os
from abc import abstractmethod, abstractproperty, ABC
from tkinter import E
from typing import NoReturn
from twocaptcha import TwoCaptcha
from urllib.parse import urlparse, parse_qs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_stealth import stealth

class BasePage(ABC):
    """
    Base class to initialize the base page that will be called from all pages
    """
    def __init__(self, captcha_api_key: str, login: str, password: str):
        logging.info("Initializing webdriver page")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--enable-javascript")
        self._login = login
        self._password = password
        self._is_docker_runner = "IS_DOCKER" in os.environ

        logging.info(f"Docker runner is set to {self._is_docker_runner}")
        self._driver = webdriver.Chrome(options=chrome_options) if not self._is_docker_runner else webdriver.Remote(options=webdriver.ChromeOptions(), command_executor="http://automation_hub:4444/wd/hub")

        logging.info(f"Driver connected to the Selenium")
        stealth(self._driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        logging.info(f"Driver set up for stealth mode")
        self._captcha_solver = TwoCaptcha(captcha_api_key)
        self._driver.get(self._auth_page)
        logging.info(f"Opened auth page {self._auth_page}")
        self._driver.implicitly_wait(30)
        self._accept_cookies_policy()
        logging.info("Page set up")

    def __del__(self):
        self._driver.close()
        self._driver.quit()

    @abstractproperty
    def _auth_page(self) -> str:
        return ''

    @abstractproperty
    def _login_input_locator(self) -> str:
        return ''

    @abstractproperty
    def _password_input_locator(self) -> str:
        return ''

    @abstractproperty
    def _login_form_locator(self) -> str:
        return ''

    @abstractproperty
    def _accept_cookies_locator(self) -> str:
        return ''

    @abstractproperty
    def _captcha_iframe(self) -> str:
        return "//iframe[starts-with(@src, 'https://www.google.com/recaptcha/api2/anchor')]"

    @property
    def _accept_cookies_button(self) -> WebElement:
        return self._get_element(self._accept_cookies_locator)

    def _accept_cookies_policy(self):
        try:
            if self._accept_cookies_locator != '':
                self._accept_cookies_button.click()
        except Exception:
            pass

    # Web elements
    @property
    def login_input(self) -> WebElement:
        return self._get_element(self._login_input_locator)

    @property
    def password_input(self) -> WebElement:
        return self._get_element(self._password_input_locator)

    @property
    def login_form_button(self) -> WebElement:
        return self._get_element(self._login_form_locator)

    @login_input.setter
    def login_input(self, login: str) -> NoReturn:
        self.login_input.clear()
        self.login_input.send_keys(login)

    @password_input.setter
    def password_input(self, password: str) -> NoReturn:
        self.password_input.clear()
        self.password_input.send_keys(password)

    @abstractproperty
    def _capthca_site_key(self) -> str:
        site_key_element = self._get_element(self._captcha_iframe)
        return parse_qs(urlparse(site_key_element.get_attribute("src")).query)['k'][0]

    @property
    def _recaptcha_response_element(self) -> WebElement:
        return self._get_element("//*[@id='g-recaptcha-response']")

    def _get_element(self, xpath: str) -> WebElement:
        return self._driver.find_element(By.XPATH, xpath)

    @abstractmethod
    def _solve_captcha(self) -> NoReturn:
        pass

    @abstractmethod
    def do_authorisation(self):
        pass

    @abstractmethod
    def run(self) -> NoReturn:
        pass