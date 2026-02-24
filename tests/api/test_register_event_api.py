import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.api.dependencies import get_register_event_use_case

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions = False)

# tests
def test_register_event_returns_200_and_status(client):
    payload = {
        "event_type": "USER_CREATED",
        "payload": {
            "user_id": 123,
            "email": "user@email.com"
        },
        "timestamp": 1700000000
    }

    response = client.post("/events", json = payload)

    assert response.status_code == 200
    
    assert "event_id" in response.json()

    assert DecisionOutcome(response.json()["status"])
    
def test_register_event_returns_422_when_payload_is_missing(client):
    payload = {
        "event_type": "USER_CREATED",
        "timestamp": 1700000000
    }

    response = client.post("/events", json = payload)

    assert response.status_code == 422
    
class BrokenRegisterEvent:
    def register_event(
        self, 
        *_
    ):
        raise RuntimeError("boom")

def test_register_event_returns_500_on_internal_error(client):
    app.dependency_overrides[get_register_event_use_case] = (lambda: BrokenRegisterEvent())
    payload = {
        "event_type": "USER_CREATED",
        "payload": {
            "user_id": 123,
            "email": "user@email.com"
        },
        "timestamp": 1700000000
    }

    response = client.post("/events", json = payload)

    assert response.status_code == 500

    assert response.json()["detail"] == "Internal server error"

    app.dependency_overrides.clear()
