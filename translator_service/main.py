from typing import Awaitable, Callable
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from logger import get_logger, request_id_ctx_var

logger = get_logger()

app = FastAPI(title="Translation Service")


@app.middleware("http")
async def logging_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = str(uuid4())
    request_id_ctx_var.set(request_id)
    message = f"{request.method} {request.url.path}"
    logger.info(message)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/healthz", tags=["Health"])
async def healthz():
    return "ok!"


@app.post("/translate", tags=["Translate"])
def create_embeddings(request: Request):
    raise NotImplementedError
