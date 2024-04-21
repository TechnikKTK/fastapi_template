import logging
import os
import shutil
import time

from fake_useragent import FakeUserAgent
from selenium.common import UnexpectedAlertPresentException, WebDriverException
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome

from app.apps.api.v1.ds.schemas import DsTaskResult, TaskStatusChoices
from app.services.ds_registrator.browser import Browser
from app.services.ds_registrator.core import DsRegistrator
from app.services.ds_registrator.types.browser import DriverOptions


logger = logging.getLogger(__name__)


def run_ds_registrator(
    ds_record_id: str,
    rucaptcha_api_key: str,
    user_photo_path: str,
    ds_body_data: dict,
) -> dict:
    pages_steps = [
        ("Personal1", "step_2"),
        ("Personal2", "step_3"),
        ("Travel", "step_4"),
        ("TravelCompanions", "step_5"),
        ("PreviousUSTravel", "step_6"),
        ("AddressPhone", "step_7"),
        ("PptVisa", "step_8"),
        ("USContact", "step_9"),
        ("Relatives", "step_10"),
        ("Spouse", "step_11"),
        ("WorkEducation1", "step_12"),
        ("WorkEducation2", "step_13"),
        ("WorkEducation3", "step_14"),
        ("SecurityandBackground1", "step_15"),
        ("SecurityandBackground2", "step_16"),
        ("SecurityandBackground3", "step_17"),
        ("SecurityandBackground4", "step_18"),
        ("SecurityandBackground5", "step_19"),
    ]
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s (%(name)s: %(lineno)d) %(levelname)s: %(message)s",
    )
    valid_data: dict = {}
    logger.info("Начало работы")
    logger.info("Создаю словарь данных из json visa")
    for key, value in ds_body_data.items():
        #logger.info(f"{key}:{value}")
        if bool(value) is None or value is None:
            logger.info(f"{key}: не заполнен или в игноре")
            continue
        value.pop("Id")
        value.pop("DsRecordId")
        valid_data.update({key: value})
    ds_registrator = DsRegistrator(
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
    ds_task_data = {
        "barcode": "",
        "errors": [],
        "final_photo_format": "png",
        "final_photo": None,
        "DsRecordId": ds_record_id,
    }
    try:
        step_1: dict = valid_data.pop("step_1")
        location: str = step_1.pop(
            "ctl00_SiteContentPlaceHolder_ucLocation_ddlLocation"
        )
        logger.info("Начинаю процесс регистрации DS-160")
        #Определение что нам нужна только пункт В (хотя в визе это уже сделано)
        step_4 = valid_data["step_4"]
        valid_data["step_4"] = {
            "ctl00_SiteContentPlaceHolder_FormView1_dlPrincipalAppTravel_ctl00_ddlPurposeOfTrip": "B"
        } | step_4
        
        ds_registrator.get_started(location)
        barcode = ds_registrator.first_get_barcode(step_1)
        ds_task_data["barcode"] = barcode
        logger.info(f"Barcode получен: {barcode}")
        session_timed_out = False

        for key, value in valid_data.items():
            logger.info(f"Обрабатываю {key}")
            #Проверка на то что данные залиты и переходим к следующей странице
            next_page_url = ds_registrator.fill_page_data(value)
            logger.info(f"текущая страница: {next_page_url}")
            ds_registrator.accept_alert()
            attempts = 10 
            #5 попыток залит данные
            while next_page_url == ds_registrator.browser.driver.current_url:
                if attempts < 1:
                    logger.warning(f"Ошибка заполнения данных на шаге {key}")
                    ds_task_data[
                        "task_status"
                    ] = TaskStatusChoices.FAILURE.value
                    errors = ds_registrator.get_error_messages_list()
                    ds_task_data["errors"] = errors
                    ds_task_data["errors"].insert(
                        0, f"Ошибка в шаге {key.split('_')[-1]}"
                    )
                    return DsTaskResult(**ds_task_data).model_dump()
                logger.info(f"Попытка заполнить данные №{attempts} для шага ({key})")
                next_page_url = ds_registrator.fill_page_data(value)
                attempts -= 1
            current_url = ds_registrator.browser.driver.current_url
            if (
                "SessionTimedOut.aspx" in current_url
                or current_url == ds_registrator.HOME_PAGE_URL
            ):
                session_timed_out = True
                logger.warning(f"Обрыв сессии на этапе {key}")
                break

        if session_timed_out:     
            ds_registrator.recover_session_time_out(
                barcode,
                valid_data["step_2"][
                    "ctl00_SiteContentPlaceHolder_FormView1_tbxAPP_SURNAME"
                ][:5],
                valid_data["step_2"][
                    "ctl00_SiteContentPlaceHolder_FormView1_tbxDOBYear"
                ],
                step_1["ctl00_SiteContentPlaceHolder_txtAnswer"],
            )
            time.sleep(3)
            current_url = ds_registrator.browser.driver.current_url
            resume_idx = None
            logger.info("Поиск последнего шага, на котором оборвалась сессия")
            for url, step in pages_steps:
                if url in current_url:
                    resume_idx = pages_steps.index((url, step))
                    break
            if resume_idx is None:
                logger.info("Шаг не найден, начинаю с 1")
                resume_idx = 1
            logger.info(f"Восстановление записи на шаге {pages_steps[resume_idx][-1]}")
            for url, step in pages_steps[resume_idx:]:
                logger.info(f"Шаг {step}")
                step_data = valid_data.get(step)
                if not step_data:
                    continue
                current_url = ds_registrator.fill_page_data(step_data)
                logger.info(f"текущая страница: {current_url}")
                attempts = 5
                while current_url == ds_registrator.browser.driver.current_url:
                    if attempts < 1:
                        logger.warning(f"Ошибка заполнения данных на шаге {step}")
                        ds_task_data[
                            "task_status"
                        ] = TaskStatusChoices.FAILURE.value
                        errors = ds_registrator.get_error_messages_list()
                        ds_task_data["errors"] = errors
                        ds_task_data["errors"].insert(
                            0, f"Ошибка в шаге {step.split('_')[-1]}"
                        )
                        return DsTaskResult(**ds_task_data).model_dump()
                    logger.info(f"Попытка заполнить данные №{attempts} для шага ({key})")
                    current_url = ds_registrator.fill_page_data(step_data)
                    attempts -= 1
                #time.sleep(3)
        
        logger.info("Заполнение анкеты DS-160 завершено, загружаю фото клиента")
        
        logger.info("#Проверка переходов (должны быть на UploadPhoto)")
        logger.info(f"Текущая страница: {ds_registrator.browser.driver.current_url}")
        ds_registrator.browser.find_elementByClass("uploadphoto").click()
        #time.sleep(7)

        logger.info("#Проверка переходов (должны быть на Upload.aspx)")
        logger.info(f"Текущая страница: {ds_registrator.browser.driver.current_url}")
        logger.info(f"Загрузка в input фото клиента")
        logger.info(f"Фото клиента: {user_photo_path}")
        ds_registrator.browser.find_elementByID("ctl00_cphMain_imageFileUpload").send_keys(user_photo_path)
        #time.sleep(4)

        logger.info(f"Нажимаю на кнопку загрузить")
        ds_registrator.browser.find_elementByID("ctl00_cphButtons_btnUpload").click()
        ds_registrator.accept_alert()        
        #time.sleep(4)
        
        logger.info("#Проверка переходов (должны быть на Result)")
        logger.info(f"Текущая страница: {ds_registrator.browser.driver.current_url}")
        ds_registrator.browser.find_elementByClass("next").click()
        ds_registrator.accept_alert()
        #time.sleep(4)

        logger.info("#Проверка переходов (должны быть на ConfirmPhoto)")
        logger.info(f"Текущая страница: {ds_registrator.browser.driver.current_url}")
        ds_registrator.browser.find_elementByClass("next").click()
        ds_registrator.accept_alert()
        #time.sleep(4)

        logger.info("#Проверка переходов (должны быть на ReviewPersonal)")
        logger.info(f"Текущая страница: {ds_registrator.browser.driver.current_url}")
        logger.info("Подтверждение введенных данных (после заполнения)")
        
        for _ in range(10):
            try:                
                ds_registrator.browser.driver.find_element(
                    By.CLASS_NAME, "next"
                ).click()
                ds_registrator.accept_alert()
               
                #Проверка переходов
                logger.info(f"Текущая страница: {ds_registrator.browser.driver.current_url}")
                
                time.sleep(5)
            except Exception as ex:
                #logger.warning(f"Ошибка {ex}")
                continue            
        time.sleep(3)
        
        logger.info("Последний шаг перед скриншотом")
        logger.info("Отмечаем чекбокс")
        ds_registrator.browser.driver.find_element(
            By.ID, "ctl00_SiteContentPlaceHolder_FormView3_rblPREP_IND_1"
        ).click()
        ds_registrator.accept_alert()
        time.sleep(3)
        logger.info("Заполняем паспортные данные из анкеты")
        ds_registrator.browser.driver.find_element(
            By.ID, "ctl00_SiteContentPlaceHolder_PPTNumTbx"
        ).send_keys(
            valid_data["step_8"][
                "ctl00_SiteContentPlaceHolder_FormView1_tbxPPT_NUM"
            ]
        )        
        logger.info("Забираем каптчу и пытаемся ее решить")
        captcha_photo = ds_registrator.browser.driver.find_element(
            By.CLASS_NAME, "LBD_CaptchaImage"
        ).screenshot_as_base64
        captcha_errors = ds_registrator.solve_captcha_2(captcha_photo)
        #Если не удалось решить капчту
        while captcha_errors:
            logger.info("Упс.. Снова решаем каптчу")
            ds_registrator.browser.driver.find_element(
                By.ID, "ctl00_SiteContentPlaceHolder_FormView3_rblPREP_IND_1"
            ).click()
            captcha_photo = ds_registrator.browser.driver.find_element(
                By.CLASS_NAME, "LBD_CaptchaImage"
            ).screenshot_as_base64
            captcha_errors = ds_registrator.solve_captcha_2(captcha_photo)
        
        ds_registrator.accept_alert()
        ds_registrator.browser.driver.find_element(
            By.CLASS_NAME, "next"
        ).click()
        ds_registrator.accept_alert()
        time.sleep(3)
    
        final_photo = ds_registrator.browser.driver.find_element(
            By.ID, "ctl00_SiteContentPlaceHolder_FormView1"
        ).screenshot_as_base64
        ds_task_data["final_photo"] = final_photo
        ds_task_data["task_status"] = TaskStatusChoices.SUCCESS.value
        
    except Exception as ex:
        logger.warning(f"Ошибка: {ex}")
        ds_task_data["task_status"] = TaskStatusChoices.FAILURE.value
    finally:
        logger.info("Пытаюсь закрыть браузер")
        try:
            logger.info("Попытка удаления процесса из памяти")

            ds_registrator.accept_alert()
            ds_registrator.browser.driver.close()            

            ds_registrator.accept_alert()
            ds_registrator.browser.driver.quit()

            ds_registrator.browser.delete()

        except (WebDriverException, UnexpectedAlertPresentException) as ex:
            logger.warning(f"Ошибка при закрытии браузера: {ex}")
        finally:
            if os.path.exists(ds_registrator.browser.driver.user_data_dir):
                if os.path.isfile(ds_registrator.browser.driver.user_data_dir):
                    os.remove(ds_registrator.browser.driver.user_data_dir)
                else:
                    shutil.rmtree(ds_registrator.browser.driver.user_data_dir)  
            
            logger.info("Возвращаю состояние таски в visa")
            return ds_task_data