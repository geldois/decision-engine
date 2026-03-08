from app.domain.entities.decisions.decision import Decision

class InMemoryDecisionRepository:
    # initializer
    def __init__(self):
        self._decisions = {}
    
    # methods

    # interface methods
    def save(
        self, 
        decision: Decision
    ) -> Decision:
        self._decisions[decision._id] = decision
        
        return decision

    def delete(
        self, 
        decision: Decision
    ) -> bool:
        if decision._id in self._decisions:
            self._decisions.pop(decision._id)

            return True
        
        return False

    def get_by_id(
        self, 
        decision_id: int
    ) -> Decision | None:
        return self._decisions.get(decision_id, None)

    def list_all(self) -> list[Decision]:
        return list(self._decisions.values())
    