import pytest
from playwright.sync_api import Page
from typing import Dict
import time
import cv2
import requests
import os as myOS
from robot.libraries.OperatingSystem import OperatingSystem
from pathlib import Path
from loguru import logger

CURDIR = Path(__file__).parent
logger.info(CURDIR)
myOS = OperatingSystem()

class Lib:
    def __init__(self, page:Page, wait_for_image):
        self.page = page
        self.wait_for_image = wait_for_image
    
    def get_image_path(self, image_name:str):
        _image_path = myOS.join_path(f"{CURDIR}/img", f"{image_name}.png")
        return _image_path
    
    def wait_image_and_click(self, image_name:str):
        """
        Wait for the image to appear on the screen and click on it
        """
        stt_img = self.wait_for_image(self.page, self.get_image_path(image_name))
        if isinstance(stt_img, tuple):
            self.page.mouse.click(stt_img[0], stt_img[1])
            time.sleep(1)
            return True
        else:
            raise Exception(f"Image {image_name} not found")
    
    def wait_and_input(self, image_name:str, text:str):
        """
        Wait for the image to appear on the screen and input text
        """
        stt_img = self.wait_for_image(self.page, self.get_image_path(image_name))
        if isinstance(stt_img, tuple):
            self.page.mouse.click(stt_img[0], stt_img[1])
            self.page.keyboard.type(text)
            return True
        else:
            raise Exception(f"Image {image_name} not found")
    
    def wait_and_verify(self, image_name:str):
        """
        Wait for the image to appear on the screen and verify
        """
        stt_img = self.wait_for_image(self.page, self.get_image_path(image_name))
        if isinstance(stt_img, tuple):
            logger.debug(f"Image {image_name} found")
            return True
        else:
            raise Exception(f"Image {image_name} not found")