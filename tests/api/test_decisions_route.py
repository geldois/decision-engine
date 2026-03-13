from fastapi.testclient import TestClient
import pytest

from app.bootstrap.container import get_event_repository, get_produce_decision_use_case
from app.domain.entities.decisions.decision_outcome import DecisionOutcome
from app.domain.entities.events.event import Event
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.main import app

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions = True)

# tests
def test_decisions_route_produce_decision_returns_200_and_valid_http_response(client):
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)
    app.dependency_overrides[get_event_repository] = lambda: event_repository
    payload = {"event_id": str(saved_event._id)}

    response = client.post("/decisions", json = payload)

    assert response.status_code == 200
    
    assert "event_id" in response.json()

    assert "rule_id" in response.json()

    assert "status" in response.json()

    assert "explanation" in response.json()

    assert "decision_id" in response.json()

    assert response.json()["event_id"] == str(saved_event._id)

    assert DecisionOutcome(response.json()["status"])

    app.dependency_overrides.clear()
    
def test_decisions_route_produce_decision_returns_422_when_event_id_is_missing(client):
    payload = {}

    response = client.post("/decisions", json = payload)

    assert response.status_code == 422
    
class BrokenProduceDecisionUseCase:
    # methods
    def produce_decision(
        self, 
        *_
    ):
        raise RuntimeError("boom")

def test_decisions_route_produce_decision_returns_500_on_internal_error(client):
    app.dependency_overrides[get_produce_decision_use_case] = (lambda: BrokenProduceDecisionUseCase())
    event = Event(
        event_type = "USER_CREATED", 
        payload = {
            "user_id": 123, 
            "email": "user@email.com"
        }, 
        timestamp = 1700000000
    )
    event_repository = InMemoryEventRepository()
    saved_event = event_repository.save(event = event)
    payload = {"event_id": str(saved_event._id)}

    response = client.post("/decisions", json = payload)

    assert response.status_code == 500

    assert response.json()["detail"] == "Internal server error"

    app.dependency_overrides.clear()
