from operator import attrgetter

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.decision_trace import DecisionTrace


class DecisionEngine:
    @staticmethod
    def decide(event: Event, rules: list[Rule]) -> Decision:
        traces: list[DecisionTrace] = []

        for rule in DecisionEngine.sort_by_priority(rules=rules):
            trace = rule.condition.evaluate(event=event)
            traces.append(trace)

            if trace.result:
                return Decision(
                    event_id=event.id,
                    rule_id=rule.id,
                    outcome=rule.outcome,
                    traces=tuple(traces),
                )

        return Decision(
            event_id=event.id,
            rule_id=None,
            outcome=DecisionOutcome.NO_MATCH,
            traces=tuple(traces),
        )

    @staticmethod
    def sort_by_priority(rules: list[Rule]) -> list[Rule]:
        return sorted(rules, key=attrgetter("priority"), reverse=True)
