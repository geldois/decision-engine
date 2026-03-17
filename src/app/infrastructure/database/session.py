from sqlalchemy import Engine
from sqlalchemy.orm import Session, sessionmaker


def get_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
