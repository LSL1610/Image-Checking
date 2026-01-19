import pytest
from playwright.sync_api import BrowserType
from typing import Dict
import time
import cv2
import os as myOS
from robot.libraries.OperatingSystem import OperatingSystem
from pathlib import Path
from loguru import logger

CURDIR = Path(__file__).resolve().parent

myOS = OperatingSystem()

DEFAULT_CONFIDENCE: float = 0.8
TIMEOUT_WAIT_IMG = 15
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
TMP_SCREENSHOT = f"{CURDIR}/tmp"
PROFILE_PATH = f"{CURDIR}/profile"
USER_DATA_DIR = "Profile_image"
# ------------------------------------------------

@pytest.fixture(scope="session")
def context(
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict,
):
    """
    You be change profile dir before run
    """

    context = browser_type.launch_persistent_context(
        # f"{PROFILE_PATH}\\{USER_DATA_DIR}",\
            None, # None is not using pro5
        **{
            **browser_type_launch_args,
            **browser_context_args,
            "slow_mo": 500,
            "headless": False,
            "ignore_https_errors": True,
            "user_agent": USER_AGENT,
            "no_viewport": True,
            "ignore_default_args": ["--enable-automation", "--no-sandbox"],
            "args": ["--start-maximized", "--disable-notifications", "--mute-audio", 
                    "--disable-infobars","--disable-save-password-bubble",
                    "--disable-features=TranslateUI","--disable-notifications",
                    "--disable-features=PasswordManager,PasswordManagerOnboarding",
                    "--disable-save-password-bubble", "--disable-credential-services",
                    "--disable-infobars",
                    "--disable-notifications",],
            # ===== Block popup / permission =====
            "permissions": [],
            "accept_downloads": False,
            # ===== Disable automation flags =====
            "ignore_default_args": [
                "--enable-automation",
                "--no-sandbox"],
        }
    )
    
    yield context
    context.close()


@pytest.fixture(scope="session")
def page(context):
    # page = context.new_page()
    # pages[0].close()
    # page = pages[1]
    pages = context.pages
    yield pages[0]


def find_image_opencv(page, template_path: str, brand: str):
    try:
        TMP = myOS.join_path(TMP_SCREENSHOT, f"{brand}_alive.png")
        page.screenshot(path=TMP)
        scr = cv2.imread(TMP)
        template = cv2.imread(template_path)
    except Exception as e:
        print(f"Please check again the path of image at: {e}")
        raise Exception("Image not found")
    else:
        """
        Change method TM_CCOEFF_NORMED detech multiple object
        For TM_CCOEFF_NORMED, larger values means good fit
        """

        width = template.shape[1]
        height = template.shape[0]
        res = cv2.matchTemplate(scr, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)

        if max_val <= DEFAULT_CONFIDENCE:
            return False

        x = max_loc[0]
        y = max_loc[1]
        threshold = max_val
        print(f"Threshold value: {threshold:.2f}")
        center_x = x + int(width / 2)  # if x and width else None
        center_y = y + int(height / 2)  # if y and height else None
        return center_x, center_y


@pytest.fixture(scope="class")
def wait_for_image():
    """Wait image with timeout.
    Returns:
        - page:Page
        - template_image: Image to wait
        - brand: image capture in tmp
    """

    def _wait(page, image_path, brand:str = "Default", timeout=TIMEOUT_WAIT_IMG):
        stop_time = time.perf_counter() + timeout
        location = None
        while time.perf_counter() < stop_time:
            try:
                location = find_image_opencv(page, image_path, brand)
                if isinstance(location, tuple):
                    print(f"[SUCCESS] Image ...{image_path} found at {location}")
                    return location
            except Exception:
                pass

            time.sleep(1)

        if location is None:
            print(f"[FAIL] {image_path}. (timeout={timeout})")
            return False

    return _wait
