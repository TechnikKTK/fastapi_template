import logging
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

from selenium.common import (
    ElementNotInteractableException,
    InvalidSelectorException,
    NoAlertPresentException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from app.services.captcha.ru_captcha import RuCaptcha
from app.services.captcha.types.ru_captcha import (
    CheckCaptchaResultParams,
    SendCaptchaBody,
    SendCaptchaMethodChoice,
)
from app.services.ds_registrator.browser import Browser


logger = logging.getLogger(__name__)


class DsRegistrator:
    HOME_PAGE_URL: str = "https://ceac.state.gov/GenNIV/Default.aspx"

    def __init__(self, browser: Browser, rucaptcha_api_key: str):
        self.browser = browser
        self.__RUCAPTCHA_API_KEY = rucaptcha_api_key

    def click_radio(self, element_id: str, value: bool):
        radio_id = element_id.replace("$", "_")
        if value:
            radio_id += "_0"
        else:
            radio_id += "_1"

        element = self.browser.find_elementByID(radio_id)
        if not element.is_displayed():
            return
        element.click()

    def set_type_values(
        self, selector: str, element_id: str, value: str | bool
    ):
        try:
            if (
                "$" in element_id
                or element_id
                == "ctl00_SiteContentPlaceHolder_FormView1_rblAddPhone"
            ):
                self.click_radio(element_id, value)
            else:
                element = self.browser.driver.find_element(
                    By.CSS_SELECTOR, selector
                )
                if not element.is_displayed():
                    return
                match element.tag_name:
                    case "select":
                        select_el = Select(element)
                        select_el.select_by_value(value)
                    case _:
                        form_type = element.get_attribute("type")
                        match form_type:
                            case "checkbox":
                                if value:
                                    if not element.is_selected():
                                        element.click()
                            case "radio":
                                self.click_radio(element_id, value)
                            case "hidden":
                                raise ValueError
                            case _:
                                element.clear()
                                #self.browser.set_input_value(selector, "")
                                element.send_keys(value)
            self.accept_alert()
        except (
            NoSuchElementException,
            InvalidSelectorException,
            ElementNotInteractableException,
            NotImplementedError,
        ):
            return

    def accept_alert(self):
        try:
            alert = self.browser.driver.switch_to.alert
            alert.accept()
        except (NoAlertPresentException, UnexpectedAlertPresentException):
            return
        
    def close_dialog(self, element_id):
        try:
            button_close_modal = self.browser.find_elementByID(element_id)        
            if button_close_modal != -1:
                
                logger.info("Кликаю на Close модального окна")
                self.browser.driver.execute_script("arguments[0].click();", button_close_modal)
                self.accept_alert()
                time.sleep(2)
        except (NoAlertPresentException, UnexpectedAlertPresentException):
            return     

    def get_error_messages_list(self) -> list[str]:
        errors = self.browser.driver.find_elements(
            By.CSS_SELECTOR,
            "#ctl00_SiteContentPlaceHolder_FormView1_ValidationSummary ul li",
        )
        return [error.text.strip().replace(".", "") for error in errors]

    @property
    def captcha_solved(self) -> bool:
        try:
            error = self.browser.driver.find_element(
                By.CSS_SELECTOR,
                "#ctl00_SiteContentPlaceHolder_ucLocation_IdentifyCaptcha1_ValidationSummary ul li",
            )
        except NoSuchElementException:
            logger.info("CAPTCHA SOLVED")
            return True
        return not error or "code" not in error.text.lower()

    def solve_captcha_2(self, file_body: str | bytes):
        captcha_solver = RuCaptcha(self.__RUCAPTCHA_API_KEY)
        response = captcha_solver.captcha_solve_request(
            SendCaptchaBody(
                self.__RUCAPTCHA_API_KEY,
                1,
                SendCaptchaMethodChoice.base64.value,
                body=file_body,
            )
        )
        if isinstance(response, str):
            if not response.startswith("OK"):
                logger.info("Каптча не решена!")
                return False
            captcha_id: int = int(response.split("|")[-1])
        else:
            try:
                captcha_id: int = int(response["request"])
            except ValueError:
                logger.info("Каптча не решена!")
                return False
        captcha_response = ""
        count = 10
        while count > 0:
            time.sleep(2)
            response = captcha_solver.check_captcha_result(
                CheckCaptchaResultParams(
                    self.__RUCAPTCHA_API_KEY, 1, captcha_id
                )
            )
            if isinstance(response, str):
                return False
            count -= 1
            if response["status"] != 1:
                logger.info("Каптча не решена!")
                continue
            else:
                captcha_response = response["request"].upper()
                break
        if count <= 0:
            return False
        
        logger.info("Каптча решена успешно!")
        self.browser.set_input_value(
            "input#ctl00_SiteContentPlaceHolder_CodeTextBox", captcha_response
        )
        self.browser.driver.find_element(
            By.ID, "ctl00_SiteContentPlaceHolder_btnSignApp"
        ).click()
        time.sleep(2)
        return self.browser.driver.find_elements(
            By.CSS_SELECTOR,
            "#ctl00_SiteContentPlaceHolder_ValidationSummary1 ul li",
        )

    def solve_captcha(self, file_body: bytes | str) -> str:
        captcha_response = "None"
        captcha_solver = RuCaptcha(self.__RUCAPTCHA_API_KEY)
        response = captcha_solver.captcha_solve_request(
            SendCaptchaBody(
                self.__RUCAPTCHA_API_KEY,
                1,
                SendCaptchaMethodChoice.base64.value,
                body=file_body,
            )
        )
        if isinstance(response, str):
            if not response.startswith("OK"):
                logger.info("Каптча не решена!")
                return captcha_response
            captcha_id: int = int(response.split("|")[-1])
        else:
            try:
                captcha_id: int = int(response["request"])
            except ValueError:
                logger.info("Каптча не решена!")
                return captcha_response
        
        count = 10
        while count > 0:
            time.sleep(2)
            response = captcha_solver.check_captcha_result(
                CheckCaptchaResultParams(
                    self.__RUCAPTCHA_API_KEY, 1, captcha_id
                )
            )
            if isinstance(response, str):
                return captcha_response
            count -= 1
            if response["status"] != 1:
                logger.info("Каптча не решена!")
                continue
            else:
                captcha_response = response["request"].upper()
                break

        return captcha_response

    def recover_session_time_out(
        self,
        barcode: str,
        surname_5_chars: str,
        birth_year: str,
        secret_q_answer: str,
    ) -> None:
        logger.info("Восстанавиливаю сессию")
        self.browser.driver.get(self.HOME_PAGE_URL)
        logger.info("Забираю каптчу")
        captcha_photo = self.browser.find_elementByClass("LBD_CaptchaImage").screenshot_as_base64
        captcha_response = self.solve_captcha(captcha_photo)
                
        while captcha_response == "None":
            logger.info("решаем новую каптчу")
            self.browser.driver.refresh()
            time.sleep(2)
            captcha_photo = self.browser.find_elementByClass("LBD_CaptchaImage").screenshot_as_base64
            captcha_response = self.solve_captcha(captcha_photo)

        logger.info(f"Rucaptcha вернул: {captcha_response}")
        logger.info("Каптча решена")
        
        logger.info("Заполняем поле решенной каптчи")
        self.new_method_setvalue("ctl00_SiteContentPlaceHolder_ucLocation_IdentifyCaptcha1_txtCodeTextBox", captcha_response)
        self.new_method_click("ctl00_SiteContentPlaceHolder_lnkRetrieve")
        
        logger.info("Заполняем поле Barcode")        
        self.new_method_setvalue("ctl00_SiteContentPlaceHolder_ApplicationRecovery1_tbxApplicationID", barcode)        
        
        logger.info("Кликаю на кнопку восстановить")        
        self.new_method_click("ctl00_SiteContentPlaceHolder_ApplicationRecovery1_btnBarcodeSubmit", 5)
        
        logger.info("Заполняю 5 перых букв Имени")        
        self.new_method_setvalue("ctl00_SiteContentPlaceHolder_ApplicationRecovery1_txbSurname", surname_5_chars)
        
        logger.info("Заполняю дату рождения")        
        self.new_method_setvalue("ctl00_SiteContentPlaceHolder_ApplicationRecovery1_txbDOBYear", birth_year)
        
        logger.info("Заполняю ответ на секретный вопрос")        
        self.new_method_setvalue("ctl00_SiteContentPlaceHolder_ApplicationRecovery1_txbAnswer", secret_q_answer)
        
        logger.info("Кликаю подвердить!")        
        self.new_method_click("ctl00_SiteContentPlaceHolder_ApplicationRecovery1_btnRetrieve",5)


    def selectDepartment(self, location_value):
        select = self.browser.find_elementByID("ctl00_SiteContentPlaceHolder_ucLocation_ddlLocation")
        if select != -1:
            logger.info("Устанавиливаю центр визы по анкете")
            self.browser.driver.find_element(
                By.CSS_SELECTOR, "option[value='%s']" % (location_value,)
            ).click()        
        time.sleep(5)


    def get_started(self, location_value: str):
        self.Location = location_value
        logger.info("Начинаю работать с сайтом департамента")
        self.browser.driver.get(self.HOME_PAGE_URL)
        logger.info(f"текущая страница: {self.browser.driver.current_url}")
        
        self.selectDepartment(location_value)
        self.close_dialog("ctl00_SiteContentPlaceHolder_ucPostMessage_ucPost_ctl01_lnkClose")

        captcha = self.browser.find_elementByClass("LBD_CaptchaImage")
        if captcha != -1:
            logger.info("Забираю скриншот для решения каптчи")
            captcha_photo = captcha.screenshot_as_base64
            captcha_response = self.solve_captcha(captcha_photo)
            logger.info(f"Rucaptcha вернул: {captcha_response}")

            while captcha_response == "None":
                logger.info("решаем новую каптчу")
                self.browser.driver.refresh()
                self.selectDepartment(location_value)
                captcha_photo = self.browser.find_elementByClass("LBD_CaptchaImage").screenshot_as_base64
                captcha_response = self.solve_captcha(captcha_photo)


            logger.info("Каптча решена")
            element = self.browser.find_elementByID("ctl00_SiteContentPlaceHolder_ucLocation_IdentifyCaptcha1_txtCodeTextBox")
            if element != -1:
                logger.info("Заполняю поле ввода каптчи")
                self.browser.set_input_value(
                    "input#ctl00_SiteContentPlaceHolder_ucLocation_IdentifyCaptcha1_txtCodeTextBox",
                    captcha_response,
                )
        
        time.sleep(3)

        button_next = self.browser.find_elementByID("ctl00_SiteContentPlaceHolder_lnkNew")
        if button_next != -1:
            logger.info("Кликаю на START AN APPLICATION")
            self.browser.driver.execute_script("arguments[0].click();", button_next)
            self.accept_alert()


    def check_timeout(self):
        if "SessionTimedOut.aspx" in self.browser.driver.current_url:
            self.browser.find_elementByClass("blankbluebutton").click()
            logger.info(f"Ошибка сессии")
            return True
        return False

    def first_get_barcode(self, second_step_data: dict) -> str:
        if self.check_timeout():
            return "-1"
        
        logger.info(f"текущая страница: {self.browser.driver.current_url}")

        logger.info("Забираем Barcode со странцы запуска департамента")
        logger.info("Отмечаем радиокнопку")
        self.new_method_click("ctl00_SiteContentPlaceHolder_chkbxPrivacyAct")
        self.accept_alert()
        time.sleep(3)

        logger.info("Копирую Barcode")
        barcode = self.browser.find_elementByID("ctl00_SiteContentPlaceHolder_lblBarcode").text
        
        for key, value in second_step_data.items():
            self.browser.set_input_value(f"#{key}", value)
            time.sleep(1)

        self.browser.find_elementByID("ctl00_SiteContentPlaceHolder_btnContinue").click()
        self.accept_alert()

        return barcode

    def sendEnter(self, id):
        element = self.browser.find_elementByID(id)
        element.sendKeys(Keys.RETURN)
        element.sendKeys(Keys.TAB)
    
    
    def fill_page_data(self, step_data: dict[str, str | None]) -> bool:
        self.accept_alert()
        page_url = self.browser.driver.current_url
        logger.info("DATA FILLING")
        for id_, value in step_data.items():
            #logger.info(f"работаю с элементом: {id_}")

            try:
                if value == None or value == "":
                    #logger.info(f"пропускаю пустой элемент: {id_}")
                    continue
                
                logger.info(f"#{id_}: {value}")
                if type(value) is int:
                    value = str(value)
                if id_.endswith("_NA"):
                    id_ = id_.replace("tbx", "cbex")
                if id_.endswith("SSN"):
                    values = value.split("-")
                    for idx in range(1, len(values) + 1):
                        self.browser.set_input_value(
                            f"#{id_}{idx}", values[idx - 1]
                        )
                else:
                    if id_ == "ctl00_SiteContentPlaceHolder_FormView1_tbxNumberOfPrevSpouses" or id_ == "ctl00_SiteContentPlaceHolder_FormView1_DListSpouse_ctl00_tbxSURNAME":
                        action = ActionChains(self.browser.driver)
                        element = self.browser.find_elementByID(id_)
                        element.clear()
                        action.click(element).perform()
                        time.sleep(3)
                        action.send_keys(value).perform()
                        time.sleep(3)
                        action.send_keys_to_element(element, Keys.ENTER).perform()
                    else:                        
                        self.set_type_values(f"#{id_}", id_, value)
                self.accept_alert()
                time.sleep(0.7)
            except Exception:
                continue
        time.sleep(3)
        try:
            self.browser.driver.find_element(
                By.ID, "ctl00_SiteContentPlaceHolder_btnChangeNationality"
            ).click()
        except (ElementNotInteractableException, NoSuchElementException):
            self.browser.driver.find_element(
                By.ID, "ctl00_SiteContentPlaceHolder_UpdateButton3"
            ).click()
        return page_url

    def new_method_click_byclass(self, id, time_wait = 0.7):
        action = ActionChains(self.browser.driver)
        element = self.browser.find_elementByClass(id)
        action.click(element).perform()
        self.accept_alert()
        time.sleep(time_wait)    

    def new_method_click(self, id, time_wait = 0.7):
        action = ActionChains(self.browser.driver)
        element = self.browser.find_elementByID(id)
        if element != -1:
            action.click(element).perform()
            time.sleep(time_wait)
        else:
            logger.error(f"Селениум не смог поднять элемент : {id}")


    def new_method_setvalue(self, id, value):
        action = ActionChains(self.browser.driver)
        element = self.browser.find_elementByID(id)
        if element != -1:
            element.clear()
            action.click(element).perform()
            time.sleep(0.3)
            action.send_keys(value).perform()
            time.sleep(0.7)
        else:
            logger.error(f"Селениум не смог поднять элемент : {id}")
