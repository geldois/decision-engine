from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.rules.rule import Rule

class RuleRepositoryContract(ABC):
    # interface methods
    @abstractmethod
    def save(
        self, 
        rule: Rule
    ) -> Rule:
        ...

    @abstractmethod
    def delete(
        self, 
        rule: Rule
    ) -> bool:
        ...
    
    @abstractmethod
    def get_by_id(
        self, 
        rule_id: UUID
    ) -> Rule | None:
        ...

    @abstractmethod
    def list_all(self) -> list[Rule]:
        ...
        