from enum import Enum

from fastapi import status


class HttpErrorCode(Enum):
    INVALID_DECISION = status.HTTP_422_UNPROCESSABLE_CONTENT
    INVALID_EVENT = status.HTTP_422_UNPROCESSABLE_CONTENT
    INVALID_RULE = status.HTTP_422_UNPROCESSABLE_CONTENT
