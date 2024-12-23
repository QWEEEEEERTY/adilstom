from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.db.models import Log
from src.db.postgres import get_session


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()
        log_dict = {"url": str(request.url),
                    "method": request.method,
                    "request_body": body.decode('utf-8') if body else "No body"}

        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk
        try:
            response_body_str = response_body.decode('utf-8') if response_body else "No body"
        except UnicodeDecodeError:
            response_body_str = "Failed to decode response body"

        rebuilt_response = Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers)
        )

        log_dict["status_code"] = response.status_code
        log_dict["response_body"] = response_body_str

        if response.status_code >= 400:
            log = Log(**log_dict)

            async for session in get_session():
                session.add(log)
                await session.commit()

        return rebuilt_response
