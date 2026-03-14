import sqlalchemy, sqlalchemy.orm

from app.bootstrap.config import DATABASE_URL, DEV_DATABASE_URL, TEST_DATABASE_URL

Base = sqlalchemy.orm.declarative_base()

# functions
def create_engine(
    database_url: str, 
    check_same_thread: bool, 
    staticpool: bool
) -> sqlalchemy.Engine:
    engine = sqlalchemy.create_engine(
        url = database_url, 
        connect_args = {"check_same_thread": check_same_thread}, 
        poolclass = sqlalchemy.StaticPool if staticpool else None
    )

    return engine

def create_session(engine: sqlalchemy.Engine) -> sqlalchemy.orm.sessionmaker[sqlalchemy.orm.Session]:
    return sqlalchemy.orm.sessionmaker(bind = engine)

def create_database(engine: sqlalchemy.Engine):
    from app.infrastructure.database.models import DecisionModel, EventModel, RuleModel

    Base.metadata.create_all(bind = engine)
