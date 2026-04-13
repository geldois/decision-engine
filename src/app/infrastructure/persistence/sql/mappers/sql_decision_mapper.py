from datetime import UTC

import app.infrastructure.serialization.decision_trace_codec as DecisionTraceCodec
from app.domain.entities.decision import Decision
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.infrastructure.database.models.decision_model import DecisionModel


def domain_to_model(decision: Decision) -> DecisionModel:
    decision_model = DecisionModel(
        id=decision.id,
        event_id=decision.event_id,
        rule_id=decision.rule_id,
        outcome=decision.outcome.value,
        traces=DecisionTraceCodec.DecisionTraceSerializer().serialize(
            traces=decision.traces
        ),
        created_at=decision.created_at,
    )

    return decision_model


def model_to_domain(decision_model: DecisionModel) -> Decision:
    created_at = (
        decision_model.created_at.replace(tzinfo=UTC)
        if decision_model.created_at.tzinfo is None
        else decision_model.created_at
    )

    decision = Decision(
        event_id=decision_model.event_id,
        rule_id=decision_model.rule_id,
        outcome=DecisionOutcome(decision_model.outcome),
        traces=DecisionTraceCodec.deserialize(traces=decision_model.traces),
        created_at=created_at,
        decision_id=decision_model.id,
    )

    return decision
