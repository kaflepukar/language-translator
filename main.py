from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response

from settings import settings
from utils.logger import get_logger, request_id_ctx_var

logger = get_logger

app = FastAPI(title="Language-Converter")


@app.middleware("http")
async def logging_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = str(uuid4())
    request_id_ctx_var.set(request_id)
    message = f"{request.method} {request.url.path}"
    extra = {}
    if settings.ENV == "local":
        extra["querry"] = request.query_params  # type ignore
    logger.info(message, extra=extra)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/health", tags=["Health"])
async def health():
    logger.info("Health check")
    return "okey"
