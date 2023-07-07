import logging
import time
import os
from tkinter import E
from typing import NoReturn
from twocaptcha import TwoCaptcha
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium_stealth import stealth

class BasePage:
    """
    Base class to initialize the base page that will be called from all pages
    """
    def __init__(self, captcha_api_key: str, login: str, password: str):
        logging.info("Initializing webdriver page")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--enable-javascript")

        # Set Chrome to automatically download files to the specified directory and disable the pdfjs viewer
        chrome_options.add_experimental_option(
            "prefs",
                {
                    "download.default_directory": "/home/seluser/Downloads",  # Set download directory.
                    "download.prompt_for_download": False,  # Automatically download files without prompting.
                    "download.directory_upgrade": True,  # Use the specified download directory.
                    "plugins.always_open_pdf_externally": True,  # Automatically open PDFs.
                    "pdfjs.disabled": True  # Disable the internal PDF viewer.
                },
        )

        self._login = login
        self._password = password
        self._is_docker_runner = "IS_DOCKER" in os.environ

        logging.info(f"Docker runner is set to {self._is_docker_runner}")
        self._driver = webdriver.Chrome(options=chrome_options) if not self._is_docker_runner else webdriver.Remote(options=chrome_options, command_executor="http://seleniarm-hub:4444/wd/hub")
        logging.info(f"Driver connected to the Selenium")
        self._captcha_solver = TwoCaptcha(captcha_api_key)


    def __del__(self):
        self._driver.close()
        self._driver.quit()

    def _get_element(self, xpath: str) -> WebElement:
        return self._driver.find_element(By.XPATH, xpath)