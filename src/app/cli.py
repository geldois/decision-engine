from os import getenv

import uvicorn
from typer import Typer

cli = Typer()


@cli.command("run")
def run():
    PORT = getenv("PORT", 8000)
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(PORT))


@cli.command("dev")
def dev():
    PORT = getenv("PORT", 8000)
    uvicorn.run("app.main:app", host="0.0.0.0", port=int(PORT), reload=True)
