from typing import Protocol

from decision_engine.application.contracts.uow import UoW


class UoWProtocol(Protocol):
    def __call__(self) -> UoW: ...
