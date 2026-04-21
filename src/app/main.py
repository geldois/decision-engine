from app.config.bootstrap import load_environment, run_migrations
from app.interface.http.app import create_app

load_environment()
run_migrations()

app = create_app()
