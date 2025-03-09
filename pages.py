import os
from loguru import logger
from playwright.sync_api import Page
from robot.libraries.OperatingSystem import OperatingSystem
import time
from pathlib import Path
from datetime import datetime
from random import randint

myOS = OperatingSystem()

ROOTDIR = Path(__file__).resolve().parents[1]
CURDIR = Path(__file__).resolve().parent

NAME_REPORT = "alive_canvas_bap"
LOGS_PATH = "logs"
CURDATE = datetime.now()

FAIL_REPORT = myOS.join_path(str(CURDIR), LOGS_PATH, f"FPT_{NAME_REPORT}.txt")

myOS.create_file(FAIL_REPORT)
logger.debug(f"\n[*] Report created at {FAIL_REPORT}")


ERRORS = {
    "Buttons": "Không bấm được nút",
    "Bar": "Đứng phiên",
    "Live": "Không hiện Video Live",
    "Banks1": "Không hiện ngân hàng",
    "QRcode": "Không hiện QR Code",
    "Cards": "Không hiện mệnh giá",
}


DELAY = randint(100, 200)
DELAY_SLEEP = randint(2, 4)
TIMEOUT = 90
FAIL_SCREENSHOT = myOS.join_path(str(CURDIR), "tmp", "Fail_bap.png")


class Bap118:
    def __init__(self, page: Page, wait_for_image, brand, fail_rp, isp="FPT") -> None:
        self.isp = isp
        self.page = page
        self.wait_for_image = wait_for_image
        self.brand = f"{brand}"
        self.fail_rp = fail_rp

    def capture_page_on_failure(self, msg_fail: str = "Fail_screenshot"):
        try:
            self.page.screenshot(path=FAIL_SCREENSHOT)
            # mb.send_photo_on_failure(FAIL_SCREENSHOT, msg_fail) # comment this line when debug
        except Exception as e:
            e = str(e)
            logger.error(f"ERR PHOTO.(LOGS={e})")

    def get_image_template_login(self, template_name):
        """Return image path with only template login name"""
        img_path = myOS.join_path(
            str(ROOTDIR), "images", self.brand, f"{template_name}.png"
        )
        return img_path

    def write_report(self, content: str):
        myOS.append_to_file(self.fail_rp, f"{content}\n")
        logger.debug(f"OK.({self.fail_rp})")

    def handle_exception_failure(self, e: Exception):
        e = str(e)
        logger.error(f"Exception: {e}")
        self.capture_page_on_failure(msg_fail=str(e))

        # self.write_report(str(e))
        assert False

    def get_template_img_and_return_status(self, template, timeout=30):
        img_template = self.get_image_template_login(template)
        return self.wait_for_image(self.page, img_template, self.brand, timeout)

    def click_button(self, template, timeout=10, function=""):
        sta = self.get_template_img_and_return_status(template, timeout)
        if not sta:
            raise Exception(f"FPT - {self.page.url} - {function}")

        self.page.mouse.click(sta[0], sta[1], delay=DELAY)
        time.sleep(2)

    def click_btn_to_access_game(self, template, function, timeout=10):
        sta = self.get_template_img_and_return_status(template, timeout)
        if isinstance(sta, tuple):
            self.page.mouse.click(sta[0], sta[1], delay=DELAY)
            return True

        raise Exception(f"FPT - {self.page.url} - {function}")

    def navigate(self, url):
        try:
            self.page.goto(url, timeout=90 * 1000)
        except TimeoutError as e:
            logger.error(f"Timed out 90s => {e}")
            # raise Exception(f"{self.page.url} => Timed out 90s")

        except Exception as e:
            logger.error(f"ERR PAGE => {e}")
            raise Exception(f"{self.page.url} => This site can not be reached")

    def click_login_btn(self, btn_login):
        self.click_button(btn_login)
        time.sleep(DELAY_SLEEP)

    def input_username(self, username_btn, username, timeout=10):
        sta = self.get_template_img_and_return_status(username_btn, timeout)
        if not sta:
            raise Exception(
                f"FPT - {self.page.url} - Login - Không tìm thấy nút tên đăng nhập."
            )
        self.page.mouse.click(sta[0] + 150, sta[1])
        time.sleep(DELAY_SLEEP)
        self.page.keyboard.press("Control+a")
        self.page.keyboard.press("Delete")
        self.page.wait_for_timeout(1000)
        time.sleep(DELAY_SLEEP)
        self.page.keyboard.type(username, delay=DELAY)

    def input_password(self, pwd_btn, pwd, timeout=10):
        sta = self.get_template_img_and_return_status(pwd_btn, timeout)
        if not sta:
            raise Exception(
                f"FPT - {self.page.url} - Login - Không tìm thấy nút điền mật khẩu."
            )
        self.page.mouse.click(sta[0] + 150, sta[1])
        time.sleep(DELAY_SLEEP)
        self.page.keyboard.type(pwd, delay=DELAY)

    def click_login_submit_btn(self, btn_login_submit, timeout=10):
        self.click_button(btn_login_submit, timeout)
        time.sleep(DELAY_SLEEP)

    def verify_login_success(self, template, timeout=90):
        sta = self.get_template_img_and_return_status(template, timeout)

        if not sta:
            logger.error("FAILED => Lỗi Đăng Nhập")
            raise Exception(f"FPT - {self.page.url} - Login - Lỗi Đăng Nhập.")

    def verify_image_game(
        self,
        template,
        function,
        timeout=90,
    ):
        """Message format: f"Access game - FPT - {function}" """
        sta = self.get_template_img_and_return_status(template, timeout)
        if not sta:
            logger.error(f"FAILED => {function}")
            raise Exception(f"{function}")

    def verify_image_banks(self, templates: list, function, timeout):
        """Message format: f"Check Nạp/Rút - FPT - {self.page.url} - {function}" """
        valid_banks = []
        for template in templates:
            sta = self.get_template_img_and_return_status(template, timeout)
            if not sta:
                sta = False
            else:
                sta = True

            valid_banks.append(sta)

        logger.info(f"{function} => {any(valid_banks)}")

        if not any(valid_banks):
            logger.error(f"FAILED => {function}")
            raise Exception(f"Check Nạp/Rút - FPT - {self.page.url} - {function}")

    def handle_click_btn_xd_bc_back_to_main(self, template1, template2):
        sta = self.get_template_img_and_return_status(template1, timeout=10)
        logger.info(f"steps 2 xoc dia, bau cua back to main: {template1}")

        if isinstance(sta, tuple):
            self.page.mouse.click(sta[0], sta[1], delay=DELAY)
            time.sleep(3)
            sta2 = self.get_template_img_and_return_status(template2, timeout=10)
            self.page.mouse.click(sta2[0], sta2[1], delay=DELAY)
            return

        self.page.reload()
        time.sleep(5)

    def verify_image_and_return_status(
        self,
        template,
        timeout=10,
    ) -> bool:
        sta = self.get_template_img_and_return_status(template, timeout)
        if not sta:
            logger.info("NEED TO LOGIN WITH PROFILE")
            return False
        else:
            logger.info("PASSED LOGIN")
            return True

    def make_login_as_profile(self, username, pwd=os.environ["PROD_PW_BAP"]):
        self.click_button("btn_login")
        self.input_username("input_username", username)
        self.input_password("input_pw", pwd)
        self.click_button("submit_login")
        return self.verify_image_and_return_status("verify_logged", timeout=30)

    def handle_click_button_when_visible(self, template1, timeout=5):
        sta = self.get_template_img_and_return_status(template1, timeout)
        if not sta:
            return

        time.sleep(1)
        self.page.mouse.click(sta[0], sta[1], delay=DELAY)

    def verify_image_bao_tri(self, template=None):
        """Check bao tri status"""
        if template is None:
            return False

        sta = self.get_template_img_and_return_status(template, 5)
        if isinstance(sta, tuple):
            logger.debug(f"Đang bảo trì => {template}")
            return True

        return False

    def handle_nap_tien_the_cao_bao_tri_and_return_status(
        self, function, template_bao_tri, template_btn_nap, msg: str = "VIETTEL"
    ):
        sta = self.verify_image_bao_tri(template_bao_tri)
        if sta:
            msg_fail = f"Check Nạp/Rút - FPT - {self.page.url} - {function} - Đang bảo trì {msg}"
            self.capture_page_on_failure(msg_fail)
            return True

        self.handle_click_button_when_visible(template_btn_nap)
        self.verify_many_templates(
            function=f"Check Nạp/Rút - FPT - {self.page.url} - {function} - Không hiển thị mệnh giá {msg}",
            prefix_template="verify_nap_the_cao",
        )

    def handle_rut_tien_the_cao_bao_tri_and_return_status(
        self, function, template_bao_tri, template_btn_nap, msg: str = "VIETTEL"
    ):
        sta = self.verify_image_bao_tri(template_bao_tri)
        logger.debug(f"status bao tri => {sta}")

        if sta:
            msg_fail = f"Check Nạp/Rút - FPT - {self.page.url} - {function} - Đang bảo trì {msg}"
            self.capture_page_on_failure(msg_fail)
            return True

        self.handle_click_button_when_visible(template_btn_nap)
        self.verify_many_templates(
            function=f"Check Nạp/Rút - FPT - {self.page.url} - {function} - Không hiển thị mệnh giá {msg}",
            prefix_template="verify_rut_the_cao",
        )

    def verify_many_templates(
        self, function, prefix_template: str = ".png", timeout=60
    ) -> bool:
        """Check all image in specify directory every 0.5s and match with prefix name.

        Args:
            function (_type_): _description_
            prefix_template (str, optional): search name image matching prefix. Defaults to ".png".
            timeout (int, optional): _description_. Defaults to 60.

        Returns:
            bool: _description_
        """
        if not isinstance(prefix_template, str):
            logger.debug(f"Only string is allow != {type({prefix_template})}")
            assert False

        BASE_PATH = myOS.join_path(str(ROOTDIR), "images", self.brand)
        IMAGES = myOS.list_files_in_directory(BASE_PATH)
        END = time.time() + timeout
        sta = None
        while time.time() <= END:
            for img in IMAGES:
                try:
                    img = myOS.join_path(BASE_PATH, img)
                    if prefix_template.lower() in img.lower():
                        sta = self.wait_for_image(
                            self.page, img, self.brand, 0.5
                        )  # changed check image timeout
                        # logger.debug(f"{img, sta}")
                        if sta:
                            logger.debug(f"FOUND IMG => {img}")
                            return True
                except Exception:
                    pass

        if sta is None:
            self.capture_page_on_failure(function)  # debug should be comment this line
            logger.error(f"{function}")
            return False

    def withdraw_cards(self):
        """Check the cao trong phan RUT tien check 2 nha mang viettel, mobi"""

        function = "Rút Tiền - Thẻ Cào"
        list_the_cao = []
        try:
            self.handle_click_button_when_visible(template1="btn_rut_the_cao")

            self.handle_click_button_when_visible(template1="btn_rut_the_cao_vt")
            vt = self.handle_rut_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri="btn_the_cao_bt_vt",
                template_btn_nap="btn_nap_vt",
                function=function,
                msg="VIETTEL",
            )
            list_the_cao.append(vt)

            self.handle_click_button_when_visible(template1="btn_rut_the_cao_vina")
            vina = self.handle_rut_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri=None,
                template_btn_nap="btn_nap_vina",
                function=function,
                msg="VINAPHONE",
            )
            list_the_cao.append(vina)

            self.handle_click_button_when_visible(template1="btn_rut_the_cao_vina")
            mobi = self.handle_rut_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri="btn_the_cao_bt_mobi",
                template_btn_nap="btn_nap_mobifone",
                function=function,
                msg="MOBIFONE",
            )
            list_the_cao.append(mobi)

            self.handle_click_button_when_visible(template1="btn_rut_the_cao_vnmobile")
            vn = self.handle_rut_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri="btn_the_cao_bt_vnmobile",
                template_btn_nap="btn_nap_vnmobile",
                function=function,
                msg="VIETNAMOBILE",
            )
            list_the_cao.append(vn)

            if all(list_the_cao):
                self.write_report(
                    content=f"Check Nạp/Rút - FPT - {self.page.url} - {function} - Tất cả thẻ cào đang bảo trì",
                )

        except Exception as e:
            self.handle_exception_failure(e)

    def deposit_cards(self):
        """Check the cao trong phan NAP tien check 2 mang viettel, mobi"""

        function = "Nạp Tiền - Thẻ Cào"
        list_the_cao = []
        try:
            logger.debug(f"Check Nạp/Rút - FPT - {self.page.url} - {function}")
            self.navigate(self.page.url)
            self.handle_click_button_when_visible(template1="btn_nap")
            self.handle_click_button_when_visible(template1="btn_nap_the_cao")
            vt = self.handle_nap_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri="btn_the_cao_bt_vt",
                template_btn_nap="btn_nap_vt",
                function=function,
                msg="VIETTEL",
            )
            list_the_cao.append(vt)

            self.handle_click_button_when_visible(template1="btn_rut_the_cao_vina")
            vina = self.handle_nap_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri=None,
                template_btn_nap="btn_nap_vina",
                function=function,
                msg="VINAPHONE",
            )
            list_the_cao.append(vina)

            self.handle_click_button_when_visible(template1="btn_rut_the_cao_vina")
            mobi = self.handle_nap_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri="btn_the_cao_bt_mobi",
                template_btn_nap="btn_nap_mobifone",
                function=function,
                msg="MOBIFONE",
            )
            list_the_cao.append(mobi)

            vn = self.handle_nap_tien_the_cao_bao_tri_and_return_status(
                template_bao_tri="btn_the_cao_bt_vnmobile",
                template_btn_nap="btn_nap_vnmobile",
                function=function,
                msg="VIETNAMOBILE",
            )
            list_the_cao.append(vn)

            if all(list_the_cao):
                self.write_report(
                    content=f"Check Nạp/Rút - FPT - {self.page.url} - {function} - Tất cả thẻ cào đang bảo trì",
                )

        except Exception as e:
            self.handle_exception_failure(e)
