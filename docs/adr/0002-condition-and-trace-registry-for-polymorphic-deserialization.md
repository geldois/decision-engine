# Registry Pattern for Polymorphic Deserialization

## Status

Accepted

## Context

`Condition` and `DecisionTrace` are polymorphic types stored as JSONB in PostgreSQL. Deserializing from a `dict` requires mapping a `"type"` string (`"simple"`, `"composite"`) to the correct Python class. The naive implementation is a chain of conditionals at each deserialization callsite:

```python
if data["type"] == "simple":
    return SimpleCondition.from_dict(data)
elif data["type"] == "composite":
    return CompositeCondition.from_dict(data)
```

This creates two problems:

1. Every deserialization site must import every concrete class. Adding a new condition type requires updating every callsite.
2. The dispatch logic is duplicated across the condition codec, the trace codec, and any future consumer that deserializes from raw data.

## Decision

Implement `ConditionRegistry` and `DecisionTraceRegistry` — class-level `dict[str, type[T]]` maps populated at module load time via a decorator applied at the bottom of each defining module:

```python
ConditionRegistry.register(name="simple")(SimpleCondition)
ConditionRegistry.register(name="composite")(CompositeCondition)
```

Deserialization callsites use only the registry:

```python
ConditionRegistry.get_class(name=data["type"]).from_dict(data=data)
```

`get_class` raises a typed domain exception (`ConditionException.condition_type_is_invalid`) for unknown type strings, making the error boundary explicit and testable.

## Consequences

- All deserialization sites are decoupled from the concrete type set — they reference only the abstract base and the registry.
- Adding a new condition type requires touching two files: the new class file and any visitor implementations that must handle the new variant.
- `get_class` makes unknown types a domain error, not a `KeyError`. The error carries an `ErrorCode` and is handled uniformly at the HTTP boundary.
- Trade-off: registration is a module-level side effect. If a module defining a concrete class is never imported, its type is silently absent from the registry. This is mitigated by placing the registration call at the bottom of the defining module — importing the class and registering it are the same action.
