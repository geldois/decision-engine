from decision_engine.config.bootstrap import load_environment, run_migrations
from decision_engine.interface.http.app import create_app

load_environment()
run_migrations()

app = create_app()
