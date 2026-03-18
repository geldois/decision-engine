from app.bootstrap.config import app_dev_settings, app_prod_settings
from app.bootstrap.wiring import create_app


app_prod = create_app(settings=app_prod_settings)
app_dev = create_app(settings=app_dev_settings)
