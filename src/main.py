from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from src.db import init_db
from src.api.endpoints import router
from src.api.middlewares import LogUnsuccessfulResponsesMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    pass

app = FastAPI(
    lifespan=lifespan,
    root_path="/zapis"
)
app.add_middleware(LogUnsuccessfulResponsesMiddleware)
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
