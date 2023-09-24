from app.config import APP_CONFIG


async def core():
    return {"status": APP_CONFIG.APP_NAME}
