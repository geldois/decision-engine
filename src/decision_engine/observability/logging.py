from __future__ import annotations

from typing import TYPE_CHECKING

import structlog
from structlog.processors import JSONRenderer

from decision_engine.observability.context import correlation_id

if TYPE_CHECKING:
    from structlog.typing import EventDict


def add_correlation_id(
    logger: object,  # noqa: ARG001
    method_name: str,  # noqa: ARG001
    event_dict: EventDict,
) -> EventDict:
    cid = correlation_id.get()

    if cid is not None:
        event_dict["correlation_id"] = str(cid)

    return event_dict


def configure_logging() -> None:
    structlog.configure(processors=[add_correlation_id, JSONRenderer()])
