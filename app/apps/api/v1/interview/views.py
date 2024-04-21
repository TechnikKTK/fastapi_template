from fastapi import Request

from app.apps.api.v1.interview.schemas import InterviewRegisterTaskCreate
from app.apps.schemas import ApiResponseStatus
from app.config import App
from app.utils.celery.selenium.tasks import interview_task


def interview_task_create(
    request: Request, body: InterviewRegisterTaskCreate
) -> ApiResponseStatus:
    app: App = request.app
    for person_data in body.persons:
        interview_task.delay(
            body.Id,
            app.config.RUCAPTCHA_API_KEY,
            body.CountryCodeShow,
            body.PostCodeShow,
            person_data.model_dump(by_alias=True),
            [date.Date for date in body.freeDates],
            app.config.app.INTERVIEW_RESULT_CALLBACK_URL,
        )
    return ApiResponseStatus(code=201, message="Задачи успешно созданы")
