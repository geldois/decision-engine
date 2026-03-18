from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from app.api.routers.decisions_router import decisions_router_factory
from app.api.routers.events_router import events_router_factory
from app.api.routers.rules_router import rules_router_factory
from app.bootstrap.config import Config
from app.bootstrap.container import Container


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app(settings: Config) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    container = Container(settings=settings)
    container.build()

    decisions_router = decisions_router_factory(
        produce_decision_handler=container.produce_decision_handler
    )
    events_router = events_router_factory(
        register_event_handler=container.register_event_handler
    )
    rules_router = rules_router_factory(
        register_rule_handler=container.register_rule_handler
    )

    app.include_router(decisions_router)
    app.include_router(events_router)
    app.include_router(rules_router)

    @app.get("/", include_in_schema=False)
    async def root():
        return RedirectResponse(url="/docs")

    @app.get("/health")
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
