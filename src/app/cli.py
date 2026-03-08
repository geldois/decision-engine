from typer import Typer
import os, uvicorn

cli = Typer()

@cli.command("run")
def run():
    PORT = os.getenv(
        "PORT", 
        8000
	)
    uvicorn.run("app.main:app", host = "0.0.0.0", port = int(PORT))

@cli.command("dev")
def dev():
    PORT = os.getenv(
        "PORT", 
        8000
	)
    uvicorn.run("app.main:app", host = "0.0.0.0", port = int(PORT), reload = True)
    