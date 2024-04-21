import enum
from dataclasses import asdict, dataclass
from typing import Literal


class SendCaptchaMethodChoice(enum.Enum):
    post = "post"
    base64 = "base64"


class SendCaptchaLang(enum.Enum):
    en = "en"
    ru = "ru"


@dataclass
class CaptchaBaseRequest:
    """
    for detail documentation see: https://rucaptcha.com/api-rucaptcha
    """

    key: str
    json: Literal[0, 1]

    def to_dict(self):
        return {
            key: value
            for key, value in asdict(self).items()
            if value is not None
        }


@dataclass
class SendCaptchaBody(CaptchaBaseRequest):
    """
    for detail documentation see: https://rucaptcha.com/api-rucaptcha
    """

    method: SendCaptchaMethodChoice
    file: str | None = None
    body: bytes | None = None
    phrase: Literal[0, 1] = 0
    regsense: Literal[0, 1] = 0
    numeric: Literal[0, 1] = 0
    calc: Literal[0, 1] = 0
    min_len: Literal[0, 1] = 0
    max_len: Literal[0, 1] = 0
    language: Literal[0, 1] = 0
    lang: SendCaptchaLang | None = None


@dataclass
class CheckCaptchaResultParams(CaptchaBaseRequest):
    """
    for detail documentation see: https://rucaptcha.com/api-rucaptcha
    """

    id: int | str
    action: Literal["get"] = "get"
    header_acao: Literal[0, 1] = 0
