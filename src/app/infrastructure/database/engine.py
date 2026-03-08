from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///:memory:"
)
engine = create_engine(
    DATABASE_URL, 
    connect_args = {"check_same_thread": False},
    poolclass = StaticPool
)
SessionLocal = sessionmaker(bind = engine)
Base = declarative_base()

# functions
def init_db():
    from app.infrastructure.database.models import DecisionModel, EventModel, RuleModel

    Base.metadata.create_all(bind = engine)
