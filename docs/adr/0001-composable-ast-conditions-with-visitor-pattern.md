# Composable AST conditions with Visitor Pattern

## Status

Accepted

## Context

The initial `Rule` implementation held a plain Python callable as its condition: `rule.condition(event) -> bool`. This
was sufficient for simple comparisons but exposed two structural problems:

1. Conditions were opaque — there was no way to inspect, serialize, or deserialize the evaluation logic without
executing it. Persisting a rule to the database meant persisting a blob that could not be reconstructed.
2. Logical combinations (AND/OR) had to be encoded as Python closures inside the callable, making the structure
invisible to any consumer outside the rule itself.

The domain also required full auditability: every decision had to carry a trace of which conditions passed or failed,
in evaluation order, including the actual vs. expected values for each comparison.

## Decision

Replace callable conditions with a recursive Abstract Syntax Tree (AST):

- `SimpleCondition` — leaf node. Holds a `field` (`EventField`), a `ComparisonOperator`, and an expected `value`.
`evaluate(event)` returns a `SimpleDecisionTrace` with the actual field value, the expected value, and the comparison
result.
- `CompositeCondition` — branch node. Holds a `LogicalOperator` (`AND` / `OR`) and a sequence of child `Condition`
nodes. `evaluate(event)` uses short-circuit evaluation via a generator passed to `LogicalOperator.evaluate`, then
returns a `CompositeDecisionTrace` containing the nested traces.

Both implement `accept(visitor)`, exposing the Visitor pattern for structural operations that must not live in the
domain — primarily JSON serialization. Codecs implement `ConditionVisitor` and `DecisionTraceVisitor` without touching
condition classes.

`DecisionTrace` mirrors the AST: `SimpleDecisionTrace` records one comparison; `CompositeDecisionTrace` records the
logical operator and a tuple of child traces. The final `Decision` holds a tuple of traces representing the full
evaluation sequence across all rules.

## Consequences

- Conditions are fully serializable to and from JSON without loss of structure. The entire rule definition round-trips
through the database as a JSONB column.
- Every decision carries a complete, recursive audit trail that reflects the evaluation tree exactly — short-circuited
branches are visible as absent traces.
- Short-circuit evaluation is structurally enforced: `LogicalOperator.evaluate` accepts a generator, so AND stops at the
first false and OR stops at the first true without special-casing.
- Adding a new condition type requires exactly three changes: implement `Condition`, register it in `ConditionRegistry`,
and add a `visit_*` method to existing visitors. No existing condition or trace code changes.
- Trade-off: the AST introduces two parallel hierarchies — one for conditions and one for traces — which must be kept
structurally consistent. A new condition type that does not produce a corresponding trace subtype breaks the symmetry.
