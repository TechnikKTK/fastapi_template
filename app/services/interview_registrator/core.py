import datetime
import logging
import random
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from app.services.captcha.ru_captcha import RuCaptcha
from app.services.captcha.types.ru_captcha import (
    CheckCaptchaResultParams,
    SendCaptchaBody,
    SendCaptchaMethodChoice,
)
from app.services.ds_registrator.browser import Browser


logger = logging.getLogger(__name__)


class InterviewRegistrator:
    HOME_PAGE_URL: str = (
        "https://evisaforms.state.gov/Instructions/SchedulingSystem.asp"
    )

    def __init__(self, browser: Browser, rucaptcha_api_key: str):
        self.browser: Browser = browser
        self.__RUCAPTCHA_API_KEY: str = rucaptcha_api_key

    def choose_country_and_city(
        self,
        country_css_selector: str,
        country_val: str,
        city_css_selector: str,
        city_val: str,
    ) -> None:
        country_select = Select(
            self.browser.driver.find_element(
                By.CSS_SELECTOR, country_css_selector
            )
        )
        country_select.select_by_value(country_val)
        time.sleep(2)
        city_select = Select(
            self.browser.driver.find_element(
                By.CSS_SELECTOR, city_css_selector
            )
        )
        city_select.select_by_value(city_val)

    def check_captcha_page_exists(self) -> bool:
        try:
            page_txt = self.browser.driver.find_element(
                By.TAG_NAME, "h4"
            ).text.lower()
            return any(
                ["type the characters" in page_txt, "try again" in page_txt]
            )
        except NoSuchElementException:
            return False

    def check_second_captcha_solved(self) -> bool:
        try:
            error = self.browser.driver.find_element(
                By.CSS_SELECTOR, "td font"
            )
        except NoSuchElementException:
            logger.info("CAPTCHA SOLVED")
            return True
        return not error or "note" not in error.text.lower()

    def solve_captcha(self, photo_selector: str) -> bool | str:
        captcha_photo = self.browser.driver.find_element(
            By.CSS_SELECTOR, photo_selector
        ).screenshot_as_base64
        captcha_solver = RuCaptcha(self.__RUCAPTCHA_API_KEY)
        response = captcha_solver.captcha_solve_request(
            SendCaptchaBody(
                self.__RUCAPTCHA_API_KEY,
                1,
                SendCaptchaMethodChoice.base64.value,
                body=captcha_photo,
            )
        )
        if not response["status"]:
            logger.info("CAPTCHA PHOTO SEND ERROR")
            return False
        captcha_id: str = response["request"]
        captcha_value = ""
        attempts = 5
        while attempts:
            time.sleep(5)
            response = captcha_solver.check_captcha_result(
                CheckCaptchaResultParams(
                    self.__RUCAPTCHA_API_KEY, 1, captcha_id
                )
            )
            if isinstance(response, str):
                logger.info("CAPTCHA NOT SOLVED")
                return False
            attempts -= 1
            if response["status"] != 1:
                logger.info("CAPTCHA NOT SOLVED YET")
                continue
            else:
                captcha_value = response["request"].upper()
                break
        if attempts <= 0:
            logger.info("CAPTCHA NOT SOLVED(ALL ATTEMPTS USED)")
            return False
        return captcha_value

    def captcha_page_exists_solve(self):
        if not self.check_captcha_page_exists():
            logger.info("NO CAPTCHA MODAL")
            return
        logger.info("CAPTCHA MODAL SOLVING")
        captcha_value = self.solve_captcha("body > img")
        attempts = 5
        while not captcha_value and attempts:
            captcha_value = self.solve_captcha("body > img")
            attempts -= 1
        if not attempts:
            return
        self.browser.driver.find_element(By.ID, "ans").send_keys(captcha_value)
        logger.info("CAPTCHA VALUE SET")
        self.browser.driver.find_element(By.ID, "jar").click()

    def maybe_captcha_page_solve(self) -> bool:
        logger.info("MAYBE CAPTCHA PAGE")
        self.captcha_page_exists_solve()
        logger.info("CAPTCHA TRIED TO SOLVE IF IT EXISTS")
        time.sleep(3)
        captcha_exists = self.check_captcha_page_exists()
        attempts = 3
        while captcha_exists and attempts:
            logger.info(
                f"CAPTCHA PAGE EXISTS! SOLVING AGAIN, ATTEMPT {attempts}"
            )
            self.captcha_page_exists_solve()
            time.sleep(3)
            captcha_exists = self.check_captcha_page_exists()
            attempts -= 1
        if not attempts:
            logger.info("CAPTCHA NOT SOLVED! NO ATTEMPTS")
            return False
        return True

    def second_page_captcha_solve(self) -> bool:
        captcha_value = self.solve_captcha("#frmconinput_CaptchaImage")
        attempts = 5
        while not captcha_value and attempts:
            captcha_value = self.solve_captcha("#frmconinput_CaptchaImage")
            attempts -= 1
        if not attempts:
            logger.info("SECOND CAPTCHA NOT SOLVED")
            return False
        logger.info("SECOND CAPTCHA SOLVED")
        self.browser.driver.find_element(By.ID, "CaptchaCode").send_keys(
            captcha_value
        )
        return True

    def set_calendar_date(self, date_str: str):
        calendar = Select(
            self.browser.driver.find_element(By.CLASS_NAME, "formfield")
        )
        calendar.select_by_value(date_str)

    def choose_calendar_day(self, date: datetime.date):
        logger.info("CHOOSING INTERVIEW DATE")
        available_days = self.browser.driver.find_elements(
            By.CSS_SELECTOR, "tr td.formfield > a"
        )
        for idx, day in enumerate(available_days):
            day = int(day.text)
            if date.day == day:
                logger.info("INTERVIEW DATE FOUND!")
                available_days[idx].click()
                return True
        return False

    def choose_interview_time(self) -> str:
        logger.info("CHOOSING INTERVIEW RANDOM TIME")
        time_inputs = self.browser.driver.find_elements(
            By.CSS_SELECTOR, ".TablebgBlack td table tbody tr td .formfield"
        )
        random_time: WebElement = random.choice(time_inputs)
        random_time.click()
        return random_time.get_attribute("value")

    def fill_input_data(self, fill_data: dict):
        logger.info("FILLING INPUT DATA")
        for key, value in fill_data.items():
            element = self.browser.driver.find_element(By.ID, key)
            input_type = element.get_attribute("type")
            if input_type == "checkbox":
                if value:
                    element.click()
            else:
                element.send_keys(value)
            time.sleep(1)

    def last_page_solve_captcha(self):
        captcha_value = self.solve_captcha("#frmconinput_CaptchaImageDiv")
        attempts = 5
        while not captcha_value and attempts:
            captcha_value = self.solve_captcha("#frmconinput_CaptchaImageDiv")
            attempts -= 1
        if not attempts:
            logger.info("LAST CAPTCHA NOT SOLVED")
            return False
        logger.info("LAST CAPTCHA SOLVED")
        self.browser.driver.find_element(By.ID, "CaptchaCode").send_keys(
            captcha_value
        )
        return True

    def last_page_has_errors(self) -> bool:
        try:
            return bool(
                self.browser.driver.find_element(
                    By.CSS_SELECTOR, "body > table > tbody > tr > td > font"
                )
            )
        except NoSuchElementException:
            return False
