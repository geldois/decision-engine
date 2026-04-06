from abc import ABC, abstractmethod


class ConditionContract(ABC):
    @abstractmethod
    def compare(self) -> bool:
        raise NotImplementedError()
