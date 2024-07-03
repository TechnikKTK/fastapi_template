from datetime import datetime

from pydantic import BaseModel

from app.apps.schemas import ApiResponseStatus


class InterviewRegisterPersons(BaseModel):
    Id: int
    link3b: str
    link8b: str
    link9b: str
    link10b: str
    link11b: str
    link12b: str
    confidentiality: bool
    privacy: bool


class AvailableDatePlaces(BaseModel):
    Available: int
    Date: datetime


class InterviewRegisterTaskCreate(BaseModel):
    Id: str
    UserId: str
    CountryCodeShow: str
    PostCodeShow: str
    persons: list[InterviewRegisterPersons]
    freeDates: list[AvailableDatePlaces]


class InterviewResponseSchema(BaseModel):
    interviewId: str
    barcode: str
    register_datetime: str | None = None
    status: ApiResponseStatus
    photo: str | None = None
    photo_format: str
