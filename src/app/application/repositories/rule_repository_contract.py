from abc import ABC, abstractmethod

from app.domain.rules.rule import Rule

class RuleRepositoryContract(ABC):
    @abstractmethod
    def list_all(self) -> list[Rule]:
        ...
        