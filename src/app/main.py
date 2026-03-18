from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from app.bootstrap.bootstrap import create_app

app = create_app("test")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


# tmp
@app.get("/health")
async def health():
    #try:
    #    session = session_factory()
    #    session.execute(text("SELECT 1"))

        return {"status": "ok"}
    #except Exception:
    #    raise HTTPException(
    #        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #        detail="Service unavailable",
    #    )
    #finally:
    #    session.close()
