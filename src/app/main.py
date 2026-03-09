from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from app.infrastructure.database.engine import init_db, SessionLocal
from app.api.routes.events_route import router as events_router

# tmp
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan = lifespan)

@app.get("/", include_in_schema = False)
async def root():
    return RedirectResponse(url = "/docs")

@app.get("/health")
async def health():
    try:
        session = SessionLocal()
        session.execute(text("SELECT 1"))

        return {"status": "ok"}
    except Exception:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail = "Service unavailable"
        )
    finally:
        session.close()

app.include_router(events_router)
