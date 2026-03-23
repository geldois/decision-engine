from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.rule import Rule


class RuleRepositoryContract(ABC):
    @abstractmethod
    def save(self, rule: Rule) -> Rule:
        raise NotImplementedError

    @abstractmethod
    def delete(self, rule: Rule) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, rule_id: UUID) -> Rule | None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[Rule]:
        raise NotImplementedError
