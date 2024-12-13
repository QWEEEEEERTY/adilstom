from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.concurrency import iterate_in_threadpool

from src.db.models import Log
from src.db.postgres import get_session


class LogUnsuccessfulResponsesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        body = await request.body()

        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        request._receive = receive

        try:
            response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            response_body = response_body[0].decode()

            if response.status_code >= 400:
                log_entry = Log(
                    url=str(request.url),
                    method=request.method,
                    request_body=body.decode("utf-8") if body else None,
                    response_body=response_body,
                    status_code=response.status_code
                )

                async for session in get_session():
                    session.add(log_entry)
                    await session.commit()

            return response
        except Exception as e:
            raise e
