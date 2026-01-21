from sqlalchemy import Column, Integer, String

from app.infrastructure.database.engine import Base

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key = True, index = True)
    event_type = Column(String, nullable = False)
    payload = Column(String, nullable = False)
    timestamp = Column(Integer, nullable = False)
