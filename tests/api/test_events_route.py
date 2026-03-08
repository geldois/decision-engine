from fastapi.testclient import TestClient
import pytest

from app.api.dependencies import get_produce_decision_use_case
from app.domain.decisions.decision_outcome import DecisionOutcome
from app.main import app

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions = True)

# tests
def test_events_route_produce_decision_returns_200_and_status(client):
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
    
def test_events_route_produce_decision_returns_422_when_payload_is_missing(client):
    payload = {
        "event_type": "USER_CREATED",
        "timestamp": 1700000000
    }

    response = client.post("/events", json = payload)

    assert response.status_code == 422
    
class BrokenProduceDecisionUseCase:
    # methods
    def produce_decision(
        self, 
        *_
    ):
        raise RuntimeError("boom")

def test_events_route_produce_decision_returns_500_on_internal_error(client):
    app.dependency_overrides[get_produce_decision_use_case] = (lambda: BrokenProduceDecisionUseCase())
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
