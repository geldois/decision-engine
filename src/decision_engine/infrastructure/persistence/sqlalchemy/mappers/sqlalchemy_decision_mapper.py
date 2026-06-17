from __future__ import annotations

from decision_engine.domain.entities.decision import Decision
from decision_engine.domain.value_objects.decision_outcome import DecisionOutcome
from decision_engine.infrastructure.persistence.sqlalchemy.codecs.decision_trace_codec import (  # noqa: E501
    DecisionTraceDeserializer,
    DecisionTraceSerializer,
)
from decision_engine.infrastructure.persistence.sqlalchemy.models.decision_model import (  # noqa: E501
    DecisionModel,
)


def domain_to_model(decision: Decision) -> DecisionModel:
    return DecisionModel(
        id=decision.id,
        event_id=decision.event_id,
        rule_id=decision.rule_id,
        outcome=decision.outcome.value,
        traces=DecisionTraceSerializer.serialize(traces=decision.traces),
        created_at=decision.created_at,
    )


def model_to_domain(decision_model: DecisionModel) -> Decision:
    return Decision(
        event_id=decision_model.event_id,
        rule_id=decision_model.rule_id,
        outcome=DecisionOutcome(decision_model.outcome),
        traces=DecisionTraceDeserializer.deserialize(data=decision_model.traces),
        created_at=decision_model.created_at,
        decision_id=decision_model.id,
    )
