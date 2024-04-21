import logging
from json import JSONDecodeError

from requests import Session

from .types.ru_captcha import CheckCaptchaResultParams, SendCaptchaBody


logger = logging.getLogger(__name__)


class RuCaptcha(Session):
    SEND_CAPTCHA_URL = "https://rucaptcha.com/in.php"
    CAPTCHA_RESULT_URL = "https://rucaptcha.com/res.php"

    def __init__(self, api_key: str):
        super().__init__()
        self.__RUCAPTCHA_API_KEY = api_key

    def captcha_solve_request(self, body: SendCaptchaBody) -> str | dict:
        response = self.post(self.SEND_CAPTCHA_URL, body.to_dict())
        logger.info("CAPTCHA SOLVE REQUEST")
        if body.json == 1:
            try:
                check_result_params = response.json()
            except JSONDecodeError as error:
                logger.error(f"RESPONSE DECODE ERROR: {error.msg}")
                check_result_params = response.text
        else:
            check_result_params = response.text
        return check_result_params

    def check_captcha_result(
        self, params: CheckCaptchaResultParams
    ) -> dict[str, str]:
        response = self.get(self.CAPTCHA_RESULT_URL, params=params.to_dict())
        logger.info("CHECK CAPTCHA RESULT REQUEST")
        return response.json()

    @property
    def api_key(self):
        return self.__RUCAPTCHA_API_KEY
