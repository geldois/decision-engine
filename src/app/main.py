from fastapi import FastAPI

from app.api.routes.events import router as events_router

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(events_router)
