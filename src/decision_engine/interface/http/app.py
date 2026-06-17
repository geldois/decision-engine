from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

from decision_engine.config.bootstrap import build_container
from decision_engine.interface.http.middleware import register_correlation_id_middleware
from decision_engine.interface.http.routers.decision_router import build_decision_router
from decision_engine.interface.http.routers.event_router import build_event_router
from decision_engine.interface.http.routers.rule_router import build_rule_router
from decision_engine.observability.logging import configure_logging

if TYPE_CHECKING:
    from decision_engine.config.container import Container, ContainerOverride
    from decision_engine.config.settings import Settings


def create_app(
    container: Container | None = None,
    settings: Settings | None = None,
    overrides: ContainerOverride | None = None,
) -> FastAPI:
    configure_logging()

    container = container or build_container(settings=settings, overrides=overrides)

    app = FastAPI()
    register_correlation_id_middleware(app=app)
    app.include_router(router=build_decision_router(container=container))
    app.include_router(router=build_event_router(container=container))
    app.include_router(router=build_rule_router(container=container))

    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:  # pyright: ignore[reportUnusedFunction]
        return RedirectResponse(url="/docs")

    @app.get("/health")
    async def health() -> dict[str, str]:  # pyright: ignore[reportUnusedFunction]
        if container.db.check_health():
            return {"status": "ok"}

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable",
        )

    return app
