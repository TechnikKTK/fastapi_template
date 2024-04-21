from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import App


class AllowedByIP(BaseHTTPMiddleware):
    def __init__(
        self,
        app: App,
        allowed_ips: list[str],
    ):
        super().__init__(app)
        self.allowed_ips = allowed_ips

    async def dispatch(self, request: Request, call_next):
        if not request.client:
            return Response("Not enough permission", status_code=403)
        if (
            "*" not in self.allowed_ips
            and request.client.host not in self.allowed_ips
        ):
            return Response("Not enough permission", status_code=403)
        response = await call_next(request)
        return response
