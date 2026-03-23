# decision-engine

[![CI](https://github.com/geldois/decision-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/geldois/decision-engine/actions)

Backend system for deterministic rule evaluation with explicit domain modeling and controlled transaction boundaries.

Live API: <https://decision-engine.angelitochagas.com>

## Design

- Explicit domain modeling (Event, Rule, Decision)
- Deterministic rule evaluation
- Clean Architecture separation
- Use-case driven application layer
- Unit of Work
- Manual dependecy injection via bootstrap (composition root)

## Testing

- Domain and application layers developed with TDD.  
- API contracts validated with automated tests.
- Test database isolated from production database

## Run

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

#### Request (swagger)

```json
{
    "event_type": "EVENT_TEST", 
    "payload": {"test": true}, 
    "timestamp": 1000000000
}
```

#### Request (terminal)

```bash
curl -v -X POST http://localhost:8000/events/ -H "Content-Type: application/json" -d '{"event_type": "EVENT_TEST", "payload": {"test": true}, "timestamp": 1000000000}'
```

#### Response

```json
{
    "event_type": "USER_CREATED", 
    "payload": {"test": true}, 
    "timestamp": 1000000000, 
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"
}
```

### Register a rule

#### Request (swagger)

```json
{
    "name": "RULE_TEST", 
    "condition_field": "event_type", 
    "condition_operator": "==", 
    "condition_value": "EVENT_TEST", 
    "outcome": "approved"
}
```

#### Request (terminal)

```bash
curl -v -X POST http://localhost:8000/rules/ -H "Content-Type: application/json" -d '{"name": "RULE_TEST", "condition_field": "event_type", "condition_operator": "==", "condition_value": "EVENT_TEST", "outcome": "approved"}'
```

#### Response

```json
{
    "name": "RULE_TEST", 
    "outcome": "approved", 
    "rule_id": "6d2d3e6c-21ef-4a0c-91b5-1a8bb0b8e3c1"
}
```

### Produce a decision

Replace the "event_id" in the /decisions request with the ID returned when registering the event.

#### Request (swagger)

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"
}
```

#### Request (terminal)

```bash
curl -v -X POST http://localhost:8000/decisions/ -H "Content-Type: application/json" -d '{"event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"}'
```

#### Response

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2",
    "rule_id": "6d2d3e6c-21ef-4a0c-91b5-1a8bb0b8e3c1",
    "status": "approved",
    "explanation": "Event <ID: 09ef7596-75ad-46e8-bb6c-eae532ce6cd2> approved",
    "decision_id": "b51b40c3-9c2c-4d2a-b7c4-7c8d3c7d3a9f"
}
```
