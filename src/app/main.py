from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from app.api.routers.decisions_router import create_decisions_router
from app.api.routers.events_router import create_events_router
from app.api.routers.rules_router import create_rules_router
from app.bootstrap.config import Config
from app.bootstrap.container import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app(settings: Config) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    container = Container(settings=settings)
    container.build()
    decisions_router = create_decisions_router(
        produce_decision_use_case=container.get_produce_decision_use_case()
    )
    events_router = create_events_router(
        register_event_use_case=container.get_register_event_use_case()
    )
    rules_router = create_rules_router(
        register_rule_use_case=container.get_register_rule_use_case()
    )
    app.include_router(decisions_router)
    app.include_router(events_router)
    app.include_router(rules_router)

    @app_prod.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app_prod.get("/health")
    async def health():
        try:
            session = container.session_factory()
            session.execute(text("SELECT 1"))

            return {"status": "ok"}
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Service unavailable",
            )
        finally:
            session.close()

    return app


settings_prod = Config("DATABASE_URL", "sqlite:///./db-prod.db")
app_prod = create_app(settings=settings_prod)
