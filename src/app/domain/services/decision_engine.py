from app.domain.entities.decisions.decision import Decision
from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.events.event import Event
from app.domain.entities.rules.rule import Rule


class DecisionEngine:
    def decide(self, event: Event, rules: list[Rule]) -> Decision:
        for rule in rules:
            if rule.applies_to(event):
                outcome = rule.outcome
                explanation = "Event <ID: " + str(event._id) + "> " + str(outcome.value)

                return Decision(
                    event_id=event._id,
                    rule_id=rule._id,
                    outcome=outcome,
                    explanation=explanation,
                )

        outcome = DecisionOutcome.NO_MATCH
        explanation = "Event <ID: " + str(event._id) + "> " + str(outcome.value)

        return Decision(
            event_id=event._id, rule_id=None, outcome=outcome, explanation=explanation
        )
