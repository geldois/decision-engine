from operator import attrgetter

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.value_objects.decision_outcome import DecisionOutcome


class DecisionEngine:
    def decide(self, event: Event, rules: list[Rule]) -> Decision:
        rules = self.sort_by_priority(rules=rules)

        for rule in rules:
            if rule.applies_to(event):
                outcome = rule.outcome
                explanation = "Event <ID: " + str(event.id) + "> " + str(outcome.value)

                return Decision(
                    event_id=event.id,
                    rule_id=rule.id,
                    outcome=outcome,
                    explanation=explanation,
                )

        outcome = DecisionOutcome.NO_MATCH
        explanation = "Event <ID: " + str(event.id) + "> " + str(outcome.value)

        return Decision(
            event_id=event.id, rule_id=None, outcome=outcome, explanation=explanation
        )

    def sort_by_priority(self, rules: list[Rule]) -> list[Rule]:
        return sorted(
            rules, key=attrgetter("priority", "created_at", "id"), reverse=True
        )
