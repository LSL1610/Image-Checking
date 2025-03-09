import os
from loguru import logger
from playwright.sync_api import Page

URL = "https://www.saucedemo.com/"

class Test_demo:
    def setup_class(self, page:Page, wait_for_imaage):
        """
        Run once for the class
        """
        self.page = page
        self.wait_for_imaage = wait_for_imaage
    
    def setup_method(self):
        """
        Run every test case
        """
        self.page.goto(URL)
        
    def test1_login(self):
        pass