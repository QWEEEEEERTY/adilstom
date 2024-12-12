from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from src.api import router
from src.db import init_db, postgres


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    pass


app = FastAPI(
    lifespan=lifespan,
    root_path="/zapis"
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fastapi-logger")


@app.middleware("http")
async def log_unsuccessful_responses(request: Request, call_next):
    session = await postgres.init_db()
    # Read and cache the request body
    body = await request.body()

    # Replace the request body so it can be read again downstream
    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    request._receive = receive

    try:
        response = await call_next(request)
        if response.status_code >= 400:
            logger.warning(
                f"Unsuccessful Response: {response.status_code} | Path: {request.url.path} | Method: {request.method} | Body: {body.decode('utf-8')}"
            )
        return response
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        raise e

app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    simplified_errors = [
        {"field": error["loc"][-1], "error": error["msg"]}
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=400,
        content={"detail": simplified_errors},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app")
