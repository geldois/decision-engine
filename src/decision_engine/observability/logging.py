from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import structlog
from structlog.dev import ConsoleRenderer
from structlog.processors import JSONRenderer
from structlog.stdlib import add_log_level

from decision_engine.observability.context import correlation_id

if TYPE_CHECKING:
    from structlog.typing import EventDict, Processor


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
    renderer: Processor = ConsoleRenderer() if sys.stdout.isatty() else JSONRenderer()
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            add_log_level,
            add_correlation_id,
            renderer,
        ]
    )
