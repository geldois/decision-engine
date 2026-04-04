# decision-engine

[![CI](https://github.com/geldois/decision-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/geldois/decision-engine/actions)

Backend system for deterministic rule evaluation with explicit domain modeling and controlled transaction boundaries.

Live API: <https://decision-engine.angelitochagas.com>

## Design

- Explicit domain modeling (Event, Rule, Decision)
- Clean Architecture separation
- Use-case driven application layer
- Unit of Work
- Manual dependecy injection via bootstrap (composition root)
- Deterministic rule evaluation with AST structure
- Conditions are stored as serialized JSON (AST structure)

## Rule Evaluation Model

Rules are evaluated using a recursive Abstract Syntax Tree (AST) structure.

Conditions are no longer flat (field/operator/value), but composable and nested:

- `SimpleCondition`: evaluates a single field against a value
- `CompositeCondition`: combines multiple conditions using logical operators (`and`, `or`)

Evaluation uses short-circuit logic (lazy evaluation), stopping as soon as the result is determined.

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
pytest
decision-engine dev
```

## Examples

### RegisterEvent

#### RegisterEventRequest (swagger)

```json
{
    "event_type": "EVENT_TEST", 
    "payload": {"test": true}, 
    "occurred_at": 1000000000
}
```

#### RegisterEventRequest (terminal)

```bash
curl -v -X POST http://localhost:8000/events/ \
-H "Content-Type: application/json" \
-d '{
    "event_type": "EVENT_TEST",
    "payload": {"test": true},
    "occurred_at": 1000000000
}'
```

#### RegisterEventResponse

```json
{
    "event_type": "EVENT_TEST", 
    "payload": {"test": true}, 
    "occurred_at": 1000000000, 
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"
}
```

### RegisterRule

#### RegisterRuleRequest (swagger)

```json
{
    "name": "RULE_TEST", 
    "condition": {
        "type": "composite",
        "operator": "and",
        "conditions": [
            {
                "type": "simple",
                "field": "event_type",
                "operator": "==",
                "value": "EVENT_TEST"
            },
            {
                "type": "composite",
                "operator": "or",
                "conditions": [
                    {
                        "type": "simple",
                        "field": "event_type",
                        "operator": "==",
                        "value": "FALSE"
                    },
                    {
                        "type": "simple",
                        "field": "payload",
                        "operator": "==",
                        "value": {"test": true}
                    }
                ]
            }
        ]
    },
    "outcome": "approved",
    "priority": 0
}
```

#### RegisterRuleRequest (terminal)

```bash
curl -v -X POST http://localhost:8000/rules/ \
-H "Content-Type: application/json" \
-d '{
    "name": "RULE_TEST",
    "condition": {
        "type": "composite",
        "operator": "and",
        "conditions": [
            {
                "type": "simple",
                "field": "event_type",
                "operator": "==",
                "value": "EVENT_TEST"
            },
            {
                "type": "composite",
                "operator": "or",
                "conditions": [
                    {
                        "type": "simple",
                        "field": "event_type",
                        "operator": "==",
                        "value": "FALSE"
                    },
                    {
                        "type": "simple",
                        "field": "payload",
                        "operator": "==",
                        "value": {"test": true}
                    }
                ]
            }
        ]
    },
    "outcome": "approved",
    "priority": 0
}'
```

#### RegisterRuleResponse

```json
{
    "name": "RULE_TEST",
    "condition": {
        "type": "composite",
        "operator": "and",
        "conditions": [
            {
                "type": "simple",
                "field": "event_type",
                "operator": "==",
                "value": "EVENT_TEST"
            },
            {
                "type": "composite",
                "operator": "or",
                "conditions": [
                    {
                        "type": "simple",
                        "field": "event_type",
                        "operator": "==",
                        "value": "FALSE"
                    },
                    {
                        "type": "simple",
                        "field": "payload",
                        "operator": "==",
                        "value": {"test": true}
                    }
                ]
            }
        ]
    },
    "outcome": "approved",
    "priority": 0,
    "rule_id": "6d2d3e6c-21ef-4a0c-91b5-1a8bb0b8e3c1"
}
```

### ProduceDecision

Replace the "event_id" in the /decisions request with the ID returned when registering the event.

#### ProduceDecisionRequest (swagger)

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"
}
```

#### ProduceDecisionRequest (terminal)

```bash
curl -v -X POST http://localhost:8000/decisions/ \
-H "Content-Type: application/json" \
-d '{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2"
}'
```

#### ProduceDecisionResponse

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2",
    "rule_id": "6d2d3e6c-21ef-4a0c-91b5-1a8bb0b8e3c1",
    "status": "approved",
    "explanation": "Event <ID: 09ef7596-75ad-46e8-bb6c-eae532ce6cd2> approved",
    "decision_id": "b51b40c3-9c2c-4d2a-b7c4-7c8d3c7d3a9f"
}
```
