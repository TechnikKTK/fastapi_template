from dataclasses import asdict
from typing import Type, Union
import logging
import os
import signal

import psutil
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .types.browser import DriverOptions

logger = logging.getLogger(__name__)

class Browser:
    def __init__(
        self, driver_type: Type[Union[Firefox, Chrome]], options: DriverOptions
    ):
        self.options = self._init_browser_options(driver_type, options)
        self.driver = driver_type(browser_executable_path="/home/ds_owner/chrome/chrome",
			driver_executable_path="/home/ds_owner/chromedriver/chromedriver", options=self.options)
        self.wait = WebDriverWait(self.driver, timeout=10, poll_frequency=0.5, ignored_exceptions=[TimeoutException])
        


    def _init_browser_options(
        self, driver_type: Type[Union[Firefox, Chrome]], options: DriverOptions
    ):
        if driver_type is Firefox:
            driver_options = FirefoxOptions()
        else:
            driver_options = ChromeOptions()
            driver_options.add_argument("--disable-notifications")
            driver_options.add_argument("--disable-popup-blocking")
        for key, value in asdict(options).items():
            if value is not None:
                setattr(driver_options, key, value)
        return driver_options

    def checkbox_set_check(self, selector: str, checked: bool):
        if checked:
            checked = "true"
        else:
            checked = "false"
        self.driver.execute_script(
            """if (document.querySelector('%s')) {
                document.querySelector('%s').checked = %s
            }"""
            % (selector, selector, checked)
        )

    def select_option(self, selector: str, value: str):
        select = Select(self.wait.until(EC.element_to_be_clickable((By.ID, selector))))
        select.select_by_value(value)
        return select

    def set_input_valueByID(self, selector: str, value: str):
        self.find_elementByID(selector)
        self.driver.execute_script(
            """if (document.querySelector('%s')) {
                document.querySelector('%s').value = '%s'
            }"""
            % (selector, selector, value)
        )
    
    def set_input_valueByClass(self, selector: str, value: str):
        self.find_elementByClass(selector)
        self.driver.execute_script(
            """if (document.querySelector('%s')) {
                document.querySelector('%s').value = '%s'
            }"""
            % (selector, selector, value)
        )

    def set_input_value(self, selector: str, value: str):
        self.driver.execute_script(
            """if (document.querySelector('%s')) {
                document.querySelector('%s').value = '%s'
            }"""
            % (selector, selector, value)
        )

    def click_clickable_elements(self, css_selector: str):
        self.driver.execute_script(
            "document.querySelectorAll('%s').forEach((el) => {el.click()})"
            % (css_selector,)
        )

    def click_clickable_element(self, css_selector: str):
        self.driver.execute_script(
            """if (document.querySelector('%s')) {
                document.querySelector('%s').click()
            }"""
            % (css_selector, css_selector)
        )

    def trim_td_blocks(self, selector: str):
        self.driver.execute_script(
            "document.querySelectorAll('%s').forEach((el) => {el.remove()})"
            % (selector,)
        )


    def delete(self):
        p = psutil.Process(self.driver.service.process.pid)
        children = p.children(recursive=True)

        # kill the chrome PIDs
        for child in children:
            try:
                logger.info(f"Закрываю дочерний процесс драйвера по PID = {child.pid}")
                os.kill(child.pid, 9)
                os.waitpid(child.pid, 0)
            except:
                pass

        try:
            logger.info(f"Закрываю процесс драйвера по PID = {p.pid}")
            os.kill(p.pid, 9)
            os.waitpid(p.pid, 0)
        except ProcessLookupError as ex:
            logger.error("Не смог закрыть хром")
            pass


    def find_elementByID(self,elementId):
        try:
            element = self.wait.until(lambda x: x.find_element(By.ID, elementId)) 
            return element
        except TimeoutException:
            return -1
        

    def find_elementByXPath(self,xPath):
        try:
            element = self.wait.until(lambda x: x.find_element(By.XPATH, xPath)) 
            return element
        except TimeoutException:
            return -1   
    
    def find_elementsByXPath(self,xPath):
        try:
            element = self.wait.until(lambda x: x.find_elements(By.XPATH, xPath)) 
            return element
        except TimeoutException:
            return -1 
        
    def find_elementsByCss(self,xPath):
        try:
            element = self.wait.until(lambda x: x.find_elements(By.CSS_SELECTOR, xPath)) 
            return element
        except TimeoutException:
            return -1 
    def find_elementByClass(self,elementClass):
        try:
            element = self.wait.until(lambda x: x.find_element(By.CLASS_NAME, elementClass)) 
            return element
        except TimeoutException:
            return -1
        
    def find_elementByCss(self,elementClass):
        try:
            element = self.wait.until(lambda x: x.find_element(By.CSS_SELECTOR, elementClass)) 
            return element
        except TimeoutException:
            return -1   