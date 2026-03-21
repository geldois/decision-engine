from dataclasses import dataclass
from typing import Callable

from sqlalchemy.orm import Session

from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)
from app.infrastructure.persistence.in_memory.unit_of_work.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)
from app.infrastructure.persistence.sql.unit_of_work.sql_unit_of_work import (
    SqlUnitOfWork,
)


@dataclass
class Container:
    in_memory_storage: InMemoryStorage | None
    session_factory: Callable[[], Session]
    unit_of_work_factory: Callable[[], InMemoryUnitOfWork | SqlUnitOfWork]
