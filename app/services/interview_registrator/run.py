import datetime
import logging
import os
import random
import shutil
import time

from fake_useragent import FakeUserAgent
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
    response_data = {
        "interviewId": interview_id,
        "barcode": parser_person_data["link3b"],
        "photo_format": "png",
    }
    logger.info("PARSED DATA VALIDATED")
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
    try:
        logger.info("REGISTRATOR CREATED")
        registrator.browser.driver.get(registrator.HOME_PAGE_URL)
        logger.info("FIRST PAGE COUNTRY")
        time.sleep(5)
        registrator.choose_country_and_city(
            f"select[name='CountryCodeShow']",
            country_code,
            f"select[name='PostCodeShow']",
            city_code,
        )
        time.sleep(1)
        registrator.browser.driver.find_element(
            By.CSS_SELECTOR, ".buttontext"
        ).click()
        time.sleep(3)
        maybe_captcha_solved = registrator.maybe_captcha_page_solve()
        if not maybe_captcha_solved:
            response_data["status"] = ApiResponseStatus(
                code=500, message="Промежуточная капча не решена"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        time.sleep(5)
        logger.info("CAPTCHA SECOND SOLVING")
        registrator.second_page_captcha_solve()
        time.sleep(1)
        registrator.browser.driver.find_element(By.ID, "link21").click()
        time.sleep(5)
        solved = registrator.check_second_captcha_solved()
        attempts = 5
        while not solved and attempts:
            logger.info("SECOND CAPTCHA SOLVED WRONG! TRYING AGAIN")
            registrator.browser.driver.find_element(
                By.CLASS_NAME, "buttontext"
            ).click()
            time.sleep(2)
            registrator.browser.driver.refresh()
            time.sleep(3)
            registrator.second_page_captcha_solve()
            time.sleep(1)
            registrator.browser.driver.find_element(By.ID, "link21").click()
            time.sleep(3)
            solved = registrator.check_second_captcha_solved()
            attempts -= 1
        if not attempts:
            logger.info("SECOND CAPTCHA SOLVED WRONG ALL TIMES")
            response_data["status"] = ApiResponseStatus(
                code=500, message="Капча не решена"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        maybe_captcha_solved = registrator.maybe_captcha_page_solve()
        if not maybe_captcha_solved:
            response_data["status"] = ApiResponseStatus(
                code=500, message="Промежуточная капча не решена"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        time.sleep(5)
        barcode = parser_person_data.pop("link3b")
        logger.info("BARCODE FILLING")
        registrator.browser.driver.find_element(By.ID, "link3b").send_keys(
            barcode
        )
        time.sleep(1)
        registrator.browser.driver.find_element(By.ID, "link4").click()
        time.sleep(5)
        maybe_captcha_solved = registrator.maybe_captcha_page_solve()
        if not maybe_captcha_solved:
            response_data["status"] = ApiResponseStatus(
                code=500, message="Промежуточная капча не решена"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        chosen_interview_date: datetime.datetime = random.choice(
            available_dates
        )
        year, month, calendar_page_date = str(chosen_interview_date).split("-")
        calendar_page_date = "1"
        month = str(int(month))
        page_value_date = f"{month}/{calendar_page_date}/{year}"
        logger.info("CHOOSING CALENDAR DATE")
        registrator.set_calendar_date(page_value_date)
        time.sleep(3)
        maybe_captcha_solved = registrator.maybe_captcha_page_solve()
        if not maybe_captcha_solved:
            response_data["status"] = ApiResponseStatus(
                code=500, message="Промежуточная капча не решена"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        logger.info(
            f"CHOOSING INTERVIEW DATE! CHOSEN DATE {chosen_interview_date}"
        )
        chosen_status = registrator.choose_calendar_day(chosen_interview_date)
        attempts = 3
        while attempts and not chosen_status:
            logger.info("INTERVIEW DATE NOT FOUND, RETRYING ANOTHER DATE")
            available_dates.remove(chosen_interview_date)
            chosen_interview_date: datetime.datetime = random.choice(
                available_dates
            )
            year, month, calendar_page_date = str(chosen_interview_date).split(
                "-"
            )
            calendar_page_date = "1"
            month = str(int(month))
            page_value_date = f"{month}/{calendar_page_date}/{year}"
            logger.info("CHOOSING CALENDAR DATE")
            registrator.set_calendar_date(page_value_date)
            time.sleep(3)
            maybe_captcha_solved = registrator.maybe_captcha_page_solve()
            if not maybe_captcha_solved:
                response_data["status"] = ApiResponseStatus(
                    code=500, message="Промежуточная капча не решена"
                )
                return InterviewResponseSchema(**response_data).model_dump(
                    by_alias=True
                )
            logger.info(
                f"CHOOSING INTERVIEW DATE! CHOSEN DATE {chosen_interview_date}"
            )
            chosen_status = registrator.choose_calendar_day(
                chosen_interview_date
            )
            attempts -= 1
            time.sleep(1)
        if not attempts:
            logger.info("INTERVIEW DATE NOT FOUND, NO ATTEMPTS")
            response_data["status"] = ApiResponseStatus(
                code=400, message="Дата для регистрации занята"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        time.sleep(5)
        logger.info("INTERVIEW REGISTER PAGE")
        chosen_interview_datetime = registrator.choose_interview_time()
        chosen_interview_datetime = datetime.datetime.strptime(
            chosen_interview_datetime, "%m/%d/%Y %I:%M:%S %p"
        )
        response_data["datetime"] = chosen_interview_datetime
        time.sleep(1)
        registrator.fill_input_data(parser_person_data)
        logger.info("ALL DATA FILLED")
        logger.info("LAST CAPTCHA SOLVING")
        page_solve_captcha = registrator.last_page_solve_captcha()
        if not page_solve_captcha:
            response_data["status"] = ApiResponseStatus(
                code=500, message="Итоговая капча не решена"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        registrator.browser.driver.find_element(By.ID, "linkSubmit").click()
        maybe_captcha_solved = registrator.maybe_captcha_page_solve()
        if not maybe_captcha_solved:
            response_data["status"] = ApiResponseStatus(
                code=500, message="Промежуточная капча не решена"
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        logger.info("CHECKING PAGE ERRORS")
        page_errors = registrator.last_page_has_errors()
        attempts = 3
        time.sleep(2)
        while page_errors and attempts:
            registrator.browser.driver.find_element(
                By.CSS_SELECTOR, ".buttontext"
            ).click()
            time.sleep(3)
            registrator.browser.driver.find_element(
                By.CSS_SELECTOR, "#linkReset"
            ).click()
            chosen_interview_datetime = registrator.choose_interview_time()
            chosen_interview_datetime = datetime.datetime.strptime(
                chosen_interview_datetime, "%m/%d/%Y %I:%M:%S %p"
            )
            response_data["datetime"] = chosen_interview_datetime
            time.sleep(1)
            registrator.fill_input_data(parser_person_data)
            logger.info("ALL DATA FILLED")
            logger.info("LAST CAPTCHA SOLVING")
            page_solve_captcha = registrator.last_page_solve_captcha()
            if not page_solve_captcha:
                response_data["status"] = ApiResponseStatus(
                    code=500, message="Итоговая капча не решена"
                )
                return InterviewResponseSchema(**response_data).model_dump(
                    by_alias=True
                )
            registrator.browser.driver.find_element(
                By.ID, "linkSubmit"
            ).click()
            maybe_captcha_solved = registrator.maybe_captcha_page_solve()
            if not maybe_captcha_solved:
                response_data["status"] = ApiResponseStatus(
                    code=400, message="Промежуточная капча не решена"
                )
                return InterviewResponseSchema(**response_data).model_dump(
                    by_alias=True
                )
            attempts -= 1
        if not attempts:
            logger.info("NO ATTEMPTS LAST PAGE")
            response_data["status"] = ApiResponseStatus(
                code=400,
                message="Попробуйте ещё раз! Убедитесь, что все введенные данные правильные",
            )
            return InterviewResponseSchema(**response_data).model_dump(
                by_alias=True
            )
        logger.info("SUCCESS SAVING SCREENSHOT")
        success_screen = registrator.browser.driver.find_element(
            By.CSS_SELECTOR,
            "body > table:nth-child(28) > tbody > tr > td > table > tbody",
        ).screenshot_as_png
        with open("data.png", "wb") as file:
            file.write(success_screen)
        response_data["photo"] = str(success_screen)
        response_data["status"] = ApiResponseStatus(
            code=200, message="Успешно записал на собеседование"
        )
        logger.info("SUCCESS FINISH")
        return InterviewResponseSchema(**response_data).model_dump(
            by_alias=True
        )
    except Exception as error:
        logger.info(f"UNEXPECTED ERROR: {error}")
        response_data["status"] = ApiResponseStatus(
            code=500,
            message="Что-то пошло не так... Попробуйте ещё раз. Убедитесь, "
            "что все введённые данные правильные",
        )
        return InterviewResponseSchema(**response_data).model_dump(
            by_alias=True
        )
    finally:
        logger.info("CLOSING BROWSER")
        registrator.browser.driver.close()
        registrator.browser.driver.quit()
        if os.path.exists(registrator.browser.driver.user_data_dir):
            if os.path.isfile(registrator.browser.driver.user_data_dir):
                os.remove(registrator.browser.driver.user_data_dir)
            else:
                shutil.rmtree(registrator.browser.driver.user_data_dir)
