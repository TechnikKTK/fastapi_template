import datetime
import logging

import requests
from celery import Task

from app.apps.api.v1.ds.schemas import (
    DsTaskFailRequestSchema,
    DsTaskStatusResponse,
    TaskStatusChoices,
)
from app.apps.schemas import ApiResponseStatus
from app.services.ds_registrator.run import run_ds_registrator
from app.services.interview_registrator.run import interview_registrator_run
from app.utils.celery.app import celery_app


logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def ds_parser_task(
    self: Task,
    result_callback_url: str,
    ds_record_id: str,
    rucaptcha_api_key: str,
    user_photo_path: str,
    task_data: dict,
) -> None:
    try:
        logger.info("DS TASK IS STARTING")
        task_result = run_ds_registrator(
            ds_record_id, rucaptcha_api_key, user_photo_path, task_data
        )
    except Exception as error:
        logger.info(f"TASK IS CLOSING... Unexpected Exception: {error}")
        status = ApiResponseStatus(
            code=500,
            message="Задача провалена, что-то пошло не так... попробуйте ещё раз, "
            "убедитесь, что введённые данные валидны",
        ).model_dump()
        logger.info("BACKEND API POST REQUEST(FAIL TASK)")
        task_result = DsTaskFailRequestSchema(
            task_id=self.request.id, status=status
        ).model_dump(by_alias=True)
        requests.post(result_callback_url, json=task_result)
        return
    logger.info("TASK RESULT")
    task_status = task_result.pop("task_status")
    task_result["task_status"] = TaskStatusChoices(task_status)
    if task_result["task_status"] == TaskStatusChoices.FAILURE:
        logger.info("TASK FAILED(400)")
        status = ApiResponseStatus(
            code=400,
            message="Задача не выполнена, попробуйте ещё раз, убедитесь "
            "что введённые данные валидны",
        )
    else:
        logger.info("TASK SUCCESS(200)")
        status = ApiResponseStatus(
            code=200, message="Задача успешно выполнена"
        )
    task_result = DsTaskStatusResponse(
        status=status,
        task_id=self.request.id,
        task_status=task_result["task_status"],
        DsRecordId=task_result.get("DsRecordId", ""),
        barcode=task_result["barcode"],
        errors=task_result["errors"],
        final_photo=task_result["final_photo"],
        final_photo_format=task_result["final_photo_format"],
    ).model_dump(by_alias=True)
    logger.info("BACKEND API POST REQUEST(SUCCESS TASK)")
    requests.post(result_callback_url, json=task_result)


@celery_app.task()
def interview_task(
    unique_id: str,
    rucaptcha_api_key: str,
    country_code: str,
    city_code: str,
    person_data: dict,
    free_dates: list[datetime.datetime],
    result_callback_url: str,
):
    logger.info("INTERVIEW TASK IS STARTING")
    data = interview_registrator_run(
        unique_id,
        rucaptcha_api_key,
        country_code,
        city_code,
        person_data,
        free_dates,
    )
    logger.info("BACKEND API POST REQUEST(SUCCESS/FAIL TASK)")
    requests.post(result_callback_url, json=data)
