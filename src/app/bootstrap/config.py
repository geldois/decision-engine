from os import getenv

DATABASE_URL = getenv("DATABASE_URL", "sqlite:///./db-prod.db")

DEV_DATABASE_URL = getenv("DEV_DATABASE_URL", "sqlite:///./db-dev.db")

TEST_DATABASE_URL = getenv("TEST_DATABASE_URL", "sqlite:///:memory:")


class Config:
    def __init__(self, database_url: str | None):

        self.database_url = database_url


settings_prod = Config(database_url=DATABASE_URL)
settings_dev = Config(database_url=DEV_DATABASE_URL)
settings_test = Config(database_url=TEST_DATABASE_URL)
