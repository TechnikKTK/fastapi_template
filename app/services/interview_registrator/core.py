import datetime
import logging
import random
import time

from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

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
        self.action = ActionChains(self.browser.driver)

    #Выбор страны и города записи
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

    #Проверка каптчи
    def check_second_captcha_solved(self) -> bool:
        try:
            error = self.browser.driver.find_element(
                By.CSS_SELECTOR, "td font"
            )
        except NoSuchElementException:
            logger.info("CAPTCHA SOLVED")
            return True
        return not error or "note" not in error.text.lower()    

    #Решение каптчи
    def ru_captcha_solve(self, photo_selector: str) -> bool | str:
        captcha_div = self.browser.find_elementByXPath(photo_selector).screenshot_as_base64
        if captcha_div != -1:
            captcha_photo = captcha_div.screenshot_as_base64            
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
                logger.info("Ошибка отправки скрина каптчи")
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
                    logger.info("Не удалось решить каптчу")
                    return False
                attempts -= 1
                if response["status"] != 1:
                    logger.info("Не удалось решить каптчу снова")
                    continue
                else:
                    captcha_value = response["request"].upper()
                    break
            if attempts <= 0:
                logger.info("Не удалось решить каптчу(попытки закончились)")
                return False
            return captcha_value
        else:
            return False

    #Проверка на то что появилась каптча (от сайта)
    def check_captcha_page_exists(self) -> bool: 
        logger.info("Проверка на всплувающую каптчу")
        element = self.browser.find_elementByXPath("//b[contains(text(),'What code is in the image?')]")
        if element != -1:
            return self.advanced_captcha_solve()
        else:
            logger.info("Повезло, капчти нет")
            return False

    #Решение дополнительной каптчи
    def advanced_captcha_solve(self):
        logger.info("Решаю дополнительную каптчу")
        captcha_value = self.ru_captcha_solve("body > img")
        attempts = 5

        while not captcha_value and attempts:
            captcha_value = self.ru_captcha_solve("body > img")
            attempts -= 1
        
        if not attempts:
            return False
        
        element = self.browser.find_elementByXPath("//input[@id='ans']")
        if element != -1:
            element.send_keys(captcha_value)
        
        logger.info("Каптча решена")
        return True

    #Проверка того что страница плохого зопроса
    def check_bad_submit(self)-> bool:
        if "BadSubmit.asp" in self.browser.driver.current_url:
            element = self.browser.find_elementByXPath("//input[@value='Back'][@class='buttontext']")
            if element != -1:
                self.action.click(element).perform()
            return True
        return False
   
    #Попытка решить каптчу за 5 проходов
    def try_captcha_solve(self, xPath_selector, xPath_textbox) -> bool:
        captcha_value = self.ru_captcha_solve(xPath_selector)
        
        attempts = 5
        while not captcha_value and attempts:
            captcha_value = self.ru_captcha_solve(xPath_selector)
            attempts -= 1

        if not attempts:
            logger.info("Не удалось решить каптчу")
            return False
        
        logger.info("Вожу данные каптчи")
        textbox = self.browser.find_elementByXPath(xPath_textbox)
        if textbox != -1:
            textbox.send_keys(captcha_value)
        else:
            return False
        
        return True

    #Установка месяца и года
    def set_calendar_date(self, date_str: str):
        calendar = Select(
            self.browser.find_elementByXPath("//select[@class='formfield']")
        )
        calendar.select_by_value(date_str)

    #Ищу окно записи
    def choose_calendar_day(self, date: datetime.date):
        available_days = self.browser.find_elementByXPath("//td[@bgcolor='#9CCFFF'][@class='formfield']//a")
        for idx, day in enumerate(available_days):
            day = int(day.text)
            if date.day == day:
                logger.info("Найдено окно для записи")
                available_days[idx].click()
                return True
        return False

    #Выбираю время записи
    def choose_interview_time(self) -> str:
        logger.info("Выбираю время для записи")
        time_inputs = self.browser.find_elementByXPath("//input[@name='availTimeSlot'][@type='radio']")
        random_time: WebElement = random.choice(time_inputs)
        random_time.click()
        return random_time.get_attribute("value")

    #Заполнение данных записи
    def fill_input_data(self, fill_data: dict):
        logger.info("Заполнение данных записи")
        for key, value in fill_data.items():
            element = self.browser.find_elementByID(key)
            input_type = element.get_attribute("type")
            if input_type == "checkbox":
                if value:
                    element.click()
            else:
                element.send_keys(value)


    # def last_page_ru_captcha_solve(self):
    #     captcha_value = self.ru_captcha_solve("#frmconinput_CaptchaImageDiv")
    #     attempts = 5
    #     while not captcha_value and attempts:
    #         captcha_value = self.ru_captcha_solve("#frmconinput_CaptchaImageDiv")
    #         attempts -= 1
    #     if not attempts:
    #         logger.info("LAST Не удалось решить каптчу")
    #         return False
    #     logger.info("LAST CAPTCHA SOLVED")
    #     self.browser.driver.find_element(By.ID, "CaptchaCode").send_keys(
    #         captcha_value
    #     )
    #     return True

    # def last_page_has_errors(self) -> bool:
    #     try:
    #         return bool(
    #             self.browser.driver.find_element(
    #                 By.CSS_SELECTOR, "body > table > tbody > tr > td > font"
    #             )
    #         )
    #     except NoSuchElementException:
    #         return False
