# decision-engine
[![CI](https://github.com/geldois/decision-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/geldois/decision-engine/actions)

Rule-based decision engine built with Clean Architecture and strict TDD.

Live API: https://decision-engine.angelitochagas.com/docs

## Design

- Explicit domain modeling (Event, Rule, Decision)
- Deterministic rule evaluation
- Clean Architecture separation
- Use-case driven application layer

## Testing

- Domain and application layers developed with TDD.  
- API contracts validated with automated tests.

## Example request

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

## Example response

```json
{
    "event_id": "09ef7596-75ad-46e8-bb6c-eae532ce6cd2", 
    "status": "no_match"
}
```

## Run locally

```bash
git clone https://github.com/geldois/decision-engine.git
cd decision-engine
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
decision-engine dev
```
