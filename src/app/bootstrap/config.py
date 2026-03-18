from os import getenv


class Config:
    def __init__(
        self, database_url: str | None = None, default_database_url: str | None = None
    ):
        self.database_url = database_url
        self.default_database_url = default_database_url

    def get_env(self):
        if self.database_url:
            return getenv(self.database_url, self.default_database_url)


app_dev_settings = Config("DEV_DATABASE_URL", "sqlite:///./db-prod.db")
app_prod_settings = Config("PROD_DATABASE_URL", "sqlite:///./db-prod.db")
app_test_settings = Config()
