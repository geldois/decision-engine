from dataclasses import FrozenInstanceError, fields
from uuid import UUID, uuid4

import pytest

from app.application.dto.register_event_dto_response import RegisterEventDtoResponse


def test_register_event_dto_response_is_immutable():
    register_event_dto_response = RegisterEventDtoResponse(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        timestamp=1700000000,
        event_id=uuid4(),
    )

    assert isinstance(register_event_dto_response.event_type, str)

    assert isinstance(register_event_dto_response.payload, dict)

    assert isinstance(register_event_dto_response.timestamp, int)

    assert isinstance(register_event_dto_response.event_id, UUID)

    assert {f.name for f in fields(RegisterEventDtoResponse)} == {
        "event_type",
        "payload",
        "timestamp",
        "event_id",
    }

    with pytest.raises(FrozenInstanceError):
        register_event_dto_response.event_type = "USER_CREATED"

    with pytest.raises(FrozenInstanceError):
        register_event_dto_response.payload = {
            "user_id": 123,
            "email": "user@email.com",
        }

    with pytest.raises(FrozenInstanceError):
        register_event_dto_response.timestamp = 1700000000

    with pytest.raises(FrozenInstanceError):
        register_event_dto_response.event_id = uuid4()
