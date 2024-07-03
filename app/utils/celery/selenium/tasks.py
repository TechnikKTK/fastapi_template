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
        logger.info("Запускаю задачу заполнения анкеты DS")
        task_result = run_ds_registrator(
            ds_record_id, rucaptcha_api_key, user_photo_path, task_data
        )
    except Exception as error:
        logger.info(f"Задача провалена с ошибкой: {error}")
        status = ApiResponseStatus(
            code=500,
            message = f"Задача провалена с ошибкой: {error}",
        ).model_dump()
        logger.info("Отправляю результат обратно на сайт Визы")
        task_result = DsTaskFailRequestSchema(
            status=status, 
            task_id=self.request.id, 
            task_status = TaskStatusChoices.CRASH,
        ).model_dump(by_alias=True)
        requests.post(result_callback_url, json=task_result)
        return
    
    logger.info("Задача завершена без сбоев на сервере")
    task_status = task_result.pop("task_status")
    task_result["task_status"] = TaskStatusChoices(task_status)
    if task_result["task_status"] == TaskStatusChoices.FAILURE:
        logger.info("Есть ошибки заполнения анкеты")
        status = ApiResponseStatus(
            code=400,
            message="Задача не выполнена, попробуйте ещё раз, убедитесь "
            "что введённые данные валидны",
        )
    else:
        logger.info("Анкета заполнена полностью")
        status = ApiResponseStatus(
            code=200, message="Задача успешно выполнена"
        )
    task_result = DsTaskStatusResponse(
        task_status=TaskStatusChoices(task_result["task_status"]),
        barcode=task_result["barcode"],
        final_photo=task_result["final_photo"],
        final_photo_format=task_result["final_photo_format"],
        errors=task_result["errors"],
        status=status,
        task_id=self.request.id,
        DsRecordId=task_result.get("DsRecordId", "")
    ).model_dump(by_alias=True)
    
    logger.info("Отправляю результат обратно на сайт Визы")    
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
    logger.info("Начинаю задачу записи")
    data = interview_registrator_run(
        unique_id,
        rucaptcha_api_key,
        country_code,
        city_code,
        person_data,
        free_dates,
    )
    logger.info("Отправляю ответ на сайт визы")
    logger.info(data)
    requests.post(result_callback_url, json=data)
