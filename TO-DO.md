# TO-DO

## Errors

- Replace the configuration and bootstrap `RuntimeError`s with a typed `infrastructure/errors/`
  hierarchy, mirroring the domain errors layer (clears the `EM101`/`EM102`/`TRY003` findings).

## Linting

- Clear the remaining `ruff` findings in `src`: deep-import `E501`, `PLW1641` (define `__hash__` on
  the value objects that override `__eq__`), `PLR0913` on the database/unit-of-work builders, and
  `RET504`.
- Clear the `ruff` findings in `tests`, most of which resolve once test modules adopt
  `from __future__ import annotations`.

## Tests

- Add `from __future__ import annotations` to every test module.
- Type the FastAPI `TestClient` responses so `basedpyright` (strict) reports zero in `tests` — the
  remaining findings are `reportUnknownMemberType` on `.post`, `.json`, and `.status_code`.
- Drop redundant suffixes from test modules and functions
  (`test_produce_decision_use_case.py` → `test_produce_decision.py`).

## Typing

- Narrow `SimpleCondition.value` from `Any` to `object`, adding explicit `isinstance` guards at the
  comparison sites.
