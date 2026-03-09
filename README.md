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

### Example request (swagger)

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

### Example request (terminal)

```bash
curl -X POST http://localhost:8000/events \
    -H "Content-Type: application/json" \
    -d '{
            "event_type": "USER_CREATED", 
            "payload": {
                "user_id": 123, 
                "email": "user@email.com"
            }, 
            "timestamp": 1700000000
        }'
```

### Example response

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2", 
    "status": "no_match"
}
```
