# decision-engine
[![CI](https://github.com/geldois/decision-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/geldois/decision-engine/actions)

Rule-based decision engine for configurable decision workflows.

Live API: https://decision-engine.angelitochagas.com

## Design

- Explicit domain modeling (Event, Rule, Decision)
- Deterministic rule evaluation
- Clean Architecture separation
- Use-case driven application layer

## Testing

- Domain and application layers developed with TDD.  
- API contracts validated with automated tests.

## Run locally

```bash
git clone https://github.com/geldois/decision-engine.git
cd decision-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
decision-engine dev
```

## Examples

### Register an event

**POST /events**

```json
{
    "event_type": "USER_CREATED", 
    "payload": {
        "user_id": 123, 
        "email": "user@email.com"
    }, 
    "timestamp": 1700000000
}
```

**Response**

```json
{
    "event_type": "USER_CREATED", 
    "payload": {
        "user_id": 123, 
        "email": "user@email.com"
    }, 
    "timestamp": 1700000000, 
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"
}
```

### Register a rule

**POST /rules**

```json
{
    "name": "ALWAYS_APPLIES", 
    "condition_field": "event_type", 
    "condition_operator": "==", 
    "condition_value": "USER_CREATED", 
    "outcome": "approved"
}
```

**Response**

```json
{
    "name": "ALWAYS_APPLIES", 
    "outcome": "approved", 
    "rule_id": "6d2d3e6c-21ef-4a0c-91b5-1a8bb0b8e3c1"
}
```

### Produce a decision

**POST /decisions**

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"
}
```

**Response**

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2",
    "rule_id": "6d2d3e6c-21ef-4a0c-91b5-1a8bb0b8e3c1",
    "status": "approved",
    "explanation": "Event <ID: 09ef7596-75ad-46e8-bb6c-eae532ce6cd2> approved",
    "decision_id": "b51b40c3-9c2c-4d2a-b7c4-7c8d3c7d3a9f"
}
```
