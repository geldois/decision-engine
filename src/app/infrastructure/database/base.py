import uuid

from sqlalchemy import UUID, Engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)


def create_base(engine: Engine):
    Base.metadata.create_all(bind=engine)
