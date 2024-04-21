from celery import Celery
import sys
import os
from app.config import Misc
from app.settings.db import RedisConfig
from app.settings.server import CeleryConfig

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

misc = Misc()
broker = RedisConfig(
    _env_file=misc.REDIS_ENV,  # type: ignore
    _case_sensitive=False,  # type: ignore
)
celery_config = CeleryConfig(
    app_name="ds_tasks",
    broker_url=broker.db_url,
)
celery_app = Celery(celery_config.app_name)
celery_app.config_from_object(celery_config)
