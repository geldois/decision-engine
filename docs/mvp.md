MVP

Decision Engine is a backend system that manages events, applies deterministic rules, and records decisions with full auditability.

Entities

Rule – Defines a condition and determines an action. Rules are deterministic.

Event – The target of rules. Provides input data (customer, amount, etc.) and defines the context.

Decision – The result of applying a rule to an event. References both the rule and the event, with an explanatory outcome.

AuditLog – Records complete information about the decision taken (who, when, why, and result).
