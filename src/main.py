from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.api.endpoints import router
from src.admin import create_admin
from src.api.middlewares import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan,)
app.add_middleware(LoggingMiddleware)
app.include_router(router)
create_admin(app)


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
