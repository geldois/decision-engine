from fastapi.testclient import TestClient
import pytest

from app.bootstrap.container import get_register_event_use_case
from app.main import app

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions = True)

# tests
def test_events_route_register_event_returns_200_and_valid_http_response(client):
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
    
    assert "event_type" in response.json()

    assert "payload" in response.json()

    assert "timestamp" in response.json()

    assert "event_id" in response.json()

    assert response.json()["event_type"] == payload["event_type"]

    # assert response.json()["payload"] == payload["payload"]

    assert response.json()["timestamp"] == payload["timestamp"]
    
def test_events_route_register_event_returns_422_when_info_is_missing(client):
    payload = {}

    response = client.post("/events", json = payload)

    assert response.status_code == 422
    
class BrokenRegisterEventUseCase:
    # methods
    def register_event(
        self, 
        *_
    ):
        raise RuntimeError("boom")

def test_events_route_register_event_returns_500_on_internal_error(client):
    app.dependency_overrides[get_register_event_use_case] = (lambda: BrokenRegisterEventUseCase())
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
