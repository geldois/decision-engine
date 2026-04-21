from app.domain.entities.decision import Decision
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.infrastructure.persistence.sqlalchemy.codecs.decision_trace_codec import (
    DecisionTraceDeserializer,
    DecisionTraceSerializer,
)
from app.infrastructure.persistence.sqlalchemy.models.decision_model import (
    DecisionModel,
)


def domain_to_model(decision: Decision) -> DecisionModel:
    decision_model = DecisionModel(
        id=decision.id,
        event_id=decision.event_id,
        rule_id=decision.rule_id,
        outcome=decision.outcome.value,
        traces=DecisionTraceSerializer.serialize(traces=decision.traces),
        created_at=decision.created_at,
    )

    return decision_model


def model_to_domain(decision_model: DecisionModel) -> Decision:
    decision = Decision(
        event_id=decision_model.event_id,
        rule_id=decision_model.rule_id,
        outcome=DecisionOutcome(decision_model.outcome),
        traces=DecisionTraceDeserializer.deserialize(data=decision_model.traces),
        created_at=decision_model.created_at,
        decision_id=decision_model.id,
    )

    return decision
