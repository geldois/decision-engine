from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.infrastructure.database.engine import init_db
from app.api.routes.events import router as events_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan = lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(events_router)
