from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from decision_engine.observability.context import correlation_id

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from fastapi import FastAPI, Request, Response


def register_correlation_id_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def set_correlation_id(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        cid = uuid4()
        correlation_id.set(cid)

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = str(cid)

        return response
