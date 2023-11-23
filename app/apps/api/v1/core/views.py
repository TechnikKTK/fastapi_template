from fastapi import Request

from app.config import App


async def core(request: Request):
    app: App = request.app
    return {"status": app.config.app.APP_NAME}
