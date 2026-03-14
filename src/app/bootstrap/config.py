import os

# environment variables
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
     "sqlite:///./db-prod.db"
)

DEV_DATABASE_URL = os.getenv(
    "DEV_DATABASE_URL", 
    "sqlite:///./db-dev.db"
)

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL", 
    "sqlite:///:memory:"
)

# classes
class Config:
    # initializer
    def __init__(
        self, 
        database_url: str
    ):
        # instance attributes
        self.database_url = database_url

# instances
settings_prod = Config(
    database_url = DATABASE_URL
)
settings_dev = Config(
    database_url = DEV_DATABASE_URL
)
settings_test = Config(
    database_url = TEST_DATABASE_URL
)
