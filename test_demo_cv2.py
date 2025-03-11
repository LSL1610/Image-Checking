import os
import pytest
from loguru import logger
from playwright.sync_api import Page
from page import Lib
from time  import sleep

URL = "https://www.saucedemo.com/"

class Test_demo:
    @pytest.fixture(autouse=True, scope="class")
    @classmethod
    def setup_class(cls, page:Page, wait_for_image):
        """
        Run once for the class
        """
        cls.page = page
        cls.wait_for_image = wait_for_image
        cls.lib = Lib(cls.page, cls.wait_for_image)
    
    def setup_method(self):
        """
        Run every test case
        """
        self.page.goto(URL)
        
    def test1_login(self):
        try:
            self.lib.wait_and_input("username", "standard_user")
            self.lib.wait_and_input("pw", "secret_sauce")
            self.lib.wait_image_and_click("log_sub")
            stt_login = self.lib.wait_and_verify("sort_product")
            if stt_login:
                logger.debug("Login success")
        except Exception as e:
            logger.error(e)