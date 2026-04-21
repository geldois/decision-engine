from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse

from app.config.bootstrap import build_container
from app.config.container import Container, ContainerOverride
from app.config.settings import Settings
from app.interface.http.routers.decision_router import build_decision_router
from app.interface.http.routers.event_router import build_event_router
from app.interface.http.routers.rule_router import build_rule_router


def create_app(
    container: Container | None = None,
    settings: Settings | None = None,
    overrides: ContainerOverride | None = None,
) -> FastAPI:
    container = container or build_container(settings=settings, overrides=overrides)

    app = FastAPI()
    app.include_router(router=build_decision_router(container=container))
    app.include_router(router=build_event_router(container=container))
    app.include_router(router=build_rule_router(container=container))

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app.get("/health")
    async def health() -> dict[str, str]:
        if container.db.check_health():
            return {"status": "ok"}

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable",
        )

    return app
