# Registry pattern for polymorphic deserialization

## Status

Accepted

## Context

`Condition` and `DecisionTrace` are polymorphic types stored as JSONB in PostgreSQL. Deserializing
from a raw dict requires mapping a `type` string (`"simple"`, `"composite"`) to the correct Python
class. The naive approach branches on the type string at each deserialization callsite and imports
every concrete class directly. This creates two problems:

1. Every callsite must know the full set of concrete types. Adding a new condition type requires
   updating every deserialization site independently.
2. The dispatch logic is duplicated across the condition codec, the trace codec, and any future
   consumer that deserializes from raw data.

## Decision

`ConditionRegistry` and `DecisionTraceRegistry` are class-level `dict[str, type[T]]` maps populated
at module load time via a decorator applied at the bottom of each defining module. Registration and
class definition coexist in the same file — importing the class and registering it are the same
action.

Deserialization callsites reference only the registry. They resolve the concrete class by name and
delegate construction to it. `get_class` raises a typed domain exception for unknown type strings,
making the error boundary explicit and testable.

## Consequences

- All deserialization sites are decoupled from the concrete type set — they reference only the
  abstract base and the registry.
- Adding a new condition type requires touching two files: the new class file and any visitor
  implementations that must handle the new variant.
- `get_class` makes unknown types a domain error, not a `KeyError`. The error carries an `ErrorCode`
  and is handled uniformly at the HTTP boundary.
- Trade-off: registration is a module-level side effect. If a module defining a concrete class is
  never imported, its type is silently absent from the registry. This is mitigated by placing the
  registration call at the bottom of the defining module.
