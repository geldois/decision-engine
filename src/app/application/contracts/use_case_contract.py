from abc import ABC
from collections.abc import Callable

from app.application.contracts.unit_of_work_contract import (
    UnitOfWorkContract,
)


class UseCaseContract(ABC):
    def __init__(self, unit_of_work_factory: Callable[..., UnitOfWorkContract]) -> None:
        self.unit_of_work_factory = unit_of_work_factory
