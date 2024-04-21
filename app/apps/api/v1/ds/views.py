import base64
import asyncio
from datetime import datetime


from fastapi import Request

from app.apps.schemas import ApiResponseStatus
from app.config import App
from app.utils.celery.selenium.tasks import ds_parser_task

from .schemas import DsTaskCreateBody, DsTaskCreatedResponse


async def ds_task_create(
    request: Request, body: DsTaskCreateBody
) -> DsTaskCreatedResponse:

    app: App = request.app
    photo_name = (
        f"{body.id}_{str(datetime.now()).replace(' ', '_').replace(':', '_').replace('.', '_')}"
        f".{body.photo_format}"
    )
    photo_path = str(app.config.misc.USER_PHOTOS_DIR / photo_name)
    ds_body_data = body.model_dump(by_alias=True)

    with open(photo_path, "wb") as file:
        file.write(base64.b64decode(body.photo))
    
    task = asyncio.run(ds_parser_task(
        app.config.app.DS_RESULT_CALLBACK_URL,
        body.steps.step_1.DsRecordId,
        app.config.RUCAPTCHA_API_KEY,
        photo_path,
        ds_body_data["steps"],
    ))

    return DsTaskCreatedResponse(
        status=ApiResponseStatus(code=201, message="Задача создана успешно"),
        task_id=task.task_id,
        DsRecordId=body.id,
    )


# async def ds_task_status(
#     task_id: str,
# ) -> DsTaskCreatedResponse | DsTaskStatusResponse:
#     task = AsyncResult(task_id)
#     if task.failed():
#         return DsTaskCreatedResponse(
#             status=ApiResponseStatus(
#                 code=500,
#                 message="Задача провалена, что-то пошло не так... попробуйте ещё раз, "
#                 "убедитесь, что введённые данные валидны",
#             ),
#             task_id=task_id,
#         )
#     elif not task.ready():
#         return DsTaskCreatedResponse(
#             status=ApiResponseStatus(code=202, message="Задача выполняется"),
#             task_id=task_id,
#         )
#     task_result: dict = task.result
#     task_status = task_result.pop("task_status")
#     task_result["task_status"] = TaskStatusChoices(task_status)
#     if task.status == TaskStatusChoices.SUCCESS:
#         if task_result["task_status"] == TaskStatusChoices.FAILURE:
#             status = ApiResponseStatus(
#                 code=400,
#                 message="Задача не выполнена, попробуйте ещё раз, убедитесь "
#                 "что введённые данные валидны",
#             )
#         else:
#             status = ApiResponseStatus(
#                 code=200, message="Задача успешно выполнена"
#             )
#     else:
#         status = ApiResponseStatus(
#             code=500,
#             message="Задача провалена, что-то пошло не так... попробуйте ещё раз, "
#             "убедитесь, что введённые данные валидны",
#         )
#     return DsTaskStatusResponse(
#         status=status,
#         task_id=task_id,
#         task_status=task_result["task_status"],
#         DsRecordId=task_result.get("DsRecordId", ""),
#         barcode=task_result["barcode"],
#         errors=task_result["errors"],
#         final_photo=task_result["final_photo"],
#         final_photo_format=task_result["final_photo_format"],
#     )
