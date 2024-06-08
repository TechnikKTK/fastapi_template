import datetime
import logging
import os
import random
import shutil
import time
import uuid


from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from fake_useragent import FakeUserAgent
from selenium.common import UnexpectedAlertPresentException, WebDriverException
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome

from app.apps.api.v1.interview.schemas import (
    InterviewRegisterPersons,
    InterviewResponseSchema,
)
from app.apps.schemas import ApiResponseStatus
from app.services.ds_registrator.browser import Browser
from app.services.ds_registrator.types.browser import DriverOptions
from app.services.interview_registrator.core import InterviewRegistrator


logger = logging.getLogger(__name__)


def SendResponseError(code, response_data, text):
    response_data["status"] = ApiResponseStatus(
        code=code, message=text
    )
    return InterviewResponseSchema(**response_data).model_dump(
        by_alias=True
    )  


def interview_registrator_run(
    interview_id: str,
    rucaptcha_api_key: str,
    country_code: str,
    city_code: str,
    person_data: dict,
    available_dates: list[datetime.datetime],
):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s (%(name)s: %(lineno)d) %(levelname)s: %(message)s",
    )
    parser_person_data = InterviewRegisterPersons(**person_data).model_dump(
        by_alias=True
    )
    parser_person_data.pop("Id")
    
    logger.info("Загружаю данные с входного json")
    response_data = {
        "interviewId": interview_id,
        "barcode": parser_person_data["link3b"],
        "photo_format": "png",
    }

    logger.info("Создаю класс регистратора записи")
    registrator = InterviewRegistrator(
        Browser(
            Chrome,
            DriverOptions(
                log_level="INFO",
                user_agent=FakeUserAgent().chrome,
                headless=True,
            ),
        ),
        rucaptcha_api_key,
    )
    logger.info("Класс регистратора на собеседование создан")

    try:
        logger.info("Создание элемента действия для клика по сайту")
        action = ActionChains(registrator.browser.driver)
        
        logger.info("Открытие стартовой страницы регистрации")
        registrator.browser.driver.get(registrator.HOME_PAGE_URL)
        
        logger.info("Выбираю страну и город")        
        element = registrator.browser.find_elementByXPath("//select[@name='CountryCodeShow']")
        if element == -1:
            return SendResponseError(510,response_data, "Не найдел элемент со списком стран")

        registrator.choose_country_and_city(
            f"select[name='CountryCodeShow']",
            country_code,
            f"select[name='PostCodeShow']",
            city_code,
        )
        
        logger.info("Нажимаю кнопку отправить")        
        element = registrator.browser.find_elementByXPath("//input[@type='submit'][@class='buttontext']")
        if element != -1:
            action.click(element).perform()
        else:
            return SendResponseError(510,response_data, "Не удалось перейти на нужную страницу")

        success_solve = registrator.check_captcha_page_exists()
        if not success_solve:
            return SendResponseError(510,response_data, "Промежуточная капча не решена")

        logger.info("Следующий этап: проверка каптчи и переход к расписанию")        
        success_solve = registrator.try_captcha_solve("//div[@id='frmconinput_CaptchaImageDiv']", "//input[@id='CaptchaCode']")
        if not success_solve:
            return SendResponseError(510,response_data, "Капчта не решена успешно после выбора страны")
        
        logger.info("Переход к расписанию")        
        element = registrator.browser.find_elementByXPath("//input[@type='submit'][@id='link21']")
        if element != -1:
            action.click(element).perform()
        else:
            return SendResponseError(510,response_data, "Не удалось найти элемент submit")

        success_solve = registrator.check_captcha_page_exists()
        if not success_solve:
            return SendResponseError(510,response_data, "Промежуточная капча не решена")
        
        logger.info("Заполняем barcode клиента")
        barcode = parser_person_data.pop("link3b") 

        element = registrator.browser.find_elementByXPath("//input[@id='link3b']")
        if element != -1:
            element.send_keys(barcode)

        element = registrator.browser.find_elementByXPath("//input[@type='submit'][@id='link4']")
        if element != -1:
            action.click(element).perform()
        
        success_solve = registrator.check_captcha_page_exists()
        if not success_solve:
            return SendResponseError(510,response_data, "Промежуточная капча не решена")
        
        chosen_status = False
        attempts = 5
        while attempts and not chosen_status:
            chosen_interview_date: datetime.datetime = random.choice(available_dates)
            year, month, calendar_page_date = str(chosen_interview_date).split("-")
            calendar_page_date = "1"
            month = str(int(month))
            page_value_date = f"{month}/{calendar_page_date}/{year}"
            
            logger.info("Выбор даты приема из указанных в заявке")
            registrator.set_calendar_date(page_value_date)

            logger.info(f"Ищу окна на указанную дату: {chosen_interview_date}")
            chosen_status = registrator.choose_calendar_day(chosen_interview_date)
            available_dates.remove(chosen_interview_date)
            attempts -= 1

        if not attempts:
            logger.info("Свободные окна для указанного периода дат не найдены")
            return SendResponseError(400,response_data, "Дата для регистрации занята")

        success_solve = registrator.check_captcha_page_exists()
        if not success_solve:
            return SendResponseError(510,response_data, "Промежуточная капча не решена")

        logger.info("Следующий этап: запись на указанную дату (время)")
        
        attempts = 4
        page_errors = True
        while page_errors and attempts:
        
            chosen_interview_datetime = registrator.choose_interview_time()
            chosen_interview_datetime = datetime.datetime.strptime(
                chosen_interview_datetime, "%m/%d/%Y %I:%M:%S %p"
            )
            response_data["datetime"] = chosen_interview_datetime

            logger.info("Заполняю остальные данные и решаю каптчу")
            registrator.fill_input_data(parser_person_data)

            success_solve = registrator.try_captcha_solve("//div[@id='frmconinput_CaptchaImageDiv']", "//input[@id='CaptchaCode']")
            if not success_solve:
                return SendResponseError(510,response_data, "Капчта не решена успешно после заполнения данных")
            
            element = registrator.browser.find_elementByXPath("//input[@id='linkSubmit']")
            if element != -1:
                action.click(element).perform()

            success_solve = registrator.check_captcha_page_exists()
            if not success_solve:
                return SendResponseError(510,response_data, "Промежуточная капча не решена")

            if registrator.check_bad_submit():
                element = registrator.browser.find_elementByXPath("//input[@type='reset']")
                if element != -1:
                    action.click(element).perform()
                attempts -= 1
            else: page_errors = False

        if not attempts:
            logger.info("Закончились попытки ввода данных")
            return SendResponseError(400,response_data, "Попробуйте ещё раз! Убедитесь, что все введенные данные правильные")
       
        logger.info("Данные заполнены успешно")
        element = registrator.browser.find_elementByXPath("//td[.//span[contains(text(),'PLEASE PRINT THIS PAGE FOR YOUR RECORD')]]")
        if element != -1:
            success_screen = element[-1].screenshot_as_png
            logger.info("Забираю скриншот экрана")

            with open(f"{response_data["barcode"]}.png", "wb") as file:
                file.write(success_screen)

            response_data["photo"] = str(success_screen)
            response_data["status"] = ApiResponseStatus(
                code=200, message="Запись на собеседование прошла спешно"
            )

            logger.info("Отправляю данные обратно визе")
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        
    except Exception as error:
        logger.info(f"Ошибка во время обработки сервиса: {error}")
        return SendResponseError(500, response_data, error)

    finally:
        try:            
            logger.info("Закрываю браузер")
            registrator.browser.driver.close()  
            registrator.browser.driver.quit()
            registrator.browser.delete()
        except (WebDriverException, UnexpectedAlertPresentException) as ex:
            logger.warning(f"Ошибка при закрытии браузера: {ex}")
        except Exception as ex:
            logger.warning(f"Ошибка при закрытии браузера: {ex}")
        finally:
            if os.path.exists(registrator.browser.driver.user_data_dir):
                if os.path.isfile(registrator.browser.driver.user_data_dir):
                    os.remove(registrator.browser.driver.user_data_dir)
                else:
                    shutil.rmtree(registrator.browser.driver.user_data_dir)
