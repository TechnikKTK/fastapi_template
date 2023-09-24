from .models import Core
from app.config import APP_CONFIG


async def core():
    Core
    return {'status': APP_CONFIG.APP_NAME}
