from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from app.api.routes.decisions_route import router as decisions_router
from app.api.routes.events_route import router as events_router
from app.api.routes.rules_route import router as rules_router
from app.infrastructure.database.engine import SessionLocal, create_database

create_database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app():
    return FastAPI(lifespan=lifespan)


app = create_app()


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health():
    try:
        session = SessionLocal()
        session.execute(text("SELECT 1"))

        return {"status": "ok"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable",
        )
    finally:
        session.close()


app.include_router(events_router)
app.include_router(rules_router)
app.include_router(decisions_router)
