from __future__ import annotations

from typing import TYPE_CHECKING

from decision_engine.application.dto.requests.register_event import (
    RegisterEventDTORequest,
)

if TYPE_CHECKING:
    from decision_engine.config.container import Container

# VALID CASES


def test_register_event_use_case_returns_valid_dto_response(
    container: Container,
) -> None:
    dto_register_event_request = RegisterEventDTORequest(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )

    dto_register_event_response = container.use_cases.register_event.execute(
        dto=dto_register_event_request
    )

    assert (
        dto_register_event_response.event_type == dto_register_event_request.event_type
    )

    assert dto_register_event_response.payload == dto_register_event_request.payload

    assert (
        dto_register_event_response.occurred_at
        == dto_register_event_request.occurred_at
    )

    assert dto_register_event_response.event_id
