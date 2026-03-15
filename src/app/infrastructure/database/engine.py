from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

Base = declarative_base()


def create_database_engine(
    database_url: str, check_same_thread: bool, staticpool: bool
) -> Engine:
    engine = create_engine(
        url=database_url,
        connect_args={"check_same_thread": check_same_thread},
        poolclass=StaticPool if staticpool else None,
    )

    return engine


def create_session_factory(
    engine: Engine,
) -> sessionmaker[Session]:
    return sessionmaker(bind=engine)


def create_database(engine: Engine):

    Base.metadata.create_all(bind=engine)
