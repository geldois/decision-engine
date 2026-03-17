from abc import ABC, abstractmethod
from typing import Callable

from app.application.contracts.dto.dto_request import DtoRequest
from app.application.contracts.dto.dto_response import DtoResponse
from app.application.contracts.unit_of_works.unit_of_work_contract import (
    UnitOfWorkContract,
)


class UseCaseContract(ABC):
    def __init__(
        self,
        unit_of_work_factory: Callable[..., UnitOfWorkContract],
    ):
        self.unit_of_work_factory = unit_of_work_factory

    @abstractmethod
    def execute(self, dto_request: DtoRequest) -> DtoResponse:
        raise NotImplementedError
