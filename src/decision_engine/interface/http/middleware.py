from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

import structlog

from decision_engine.observability.context import correlation_id

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from fastapi import FastAPI, Request, Response

logger = structlog.get_logger()


def register_correlation_id_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def set_correlation_id(  # pyright: ignore[reportUnusedFunction]
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        cid = uuid4()
        correlation_id.set(cid)

        logger.info("http.request", method=request.method, path=request.url.path)
        response = await call_next(request)
        logger.info(
            "http.response",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        )
        response.headers["X-Correlation-ID"] = str(cid)

        return response
