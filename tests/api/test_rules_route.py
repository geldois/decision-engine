from fastapi.testclient import TestClient
import pytest

from app.api.dependencies import get_register_rule_use_case
from app.main import app

@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions = True)

# tests
def test_rules_route_register_rule_returns_200_and_valid_http_response(client):
    payload = {
        "name": "ALWAYS_APPLIES", 
        "condition_field": "event_type", 
        "condition_operator": "==", 
        "condition_value": "USER_CREATED", 
        "outcome": "approved"
    }

    response = client.post("/rules", json = payload)

    assert response.status_code == 200
    
    assert "name" in response.json()

    assert "outcome" in response.json()

    assert "rule_id" in response.json()

    assert response.json()["name"] == payload["name"]

    assert response.json()["outcome"] == payload["outcome"]
    
def test_rules_route_register_rule_returns_422_when_info_is_missing(client):
    payload = {}

    response = client.post("/rules", json = payload)

    assert response.status_code == 422
    
class BrokenRegisterRuleUseCase:
    # methods
    def register_rule(
        self, 
        *_
    ):
        raise RuntimeError("boom")

def test_rules_route_register_rule_returns_500_on_internal_error(client):
    app.dependency_overrides[get_register_rule_use_case] = (lambda: BrokenRegisterRuleUseCase())
    payload = {
        "name": "ALWAYS_APPLIES", 
        "condition_field": "event_type", 
        "condition_operator": "==", 
        "condition_value": "USER_CREATED", 
        "outcome": "approved"
    }

    response = client.post("/rules", json = payload)

    assert response.status_code == 500

    assert response.json()["detail"] == "Internal server error"

    app.dependency_overrides.clear()
