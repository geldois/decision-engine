from fastapi import status

from app.domain.exceptions.domain_exception import DomainException

_MAPPING: dict[str, int] = {
    "DECISION_EXPLANATION_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "DECISION_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "DECISION_OUTCOME_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "EVENT_PAYLOAD_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_TIMESTAMP_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "EVENT_TYPE_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "RULE_CONDITION_INVALID": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "RULE_CONDITION_VALUE_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "RULE_NAME_EMPTY": status.HTTP_422_UNPROCESSABLE_CONTENT,
    "RULE_NOT_FOUND": status.HTTP_404_NOT_FOUND,
}


def map_domain_exception_to_http_error_code(domain_exception: DomainException) -> int:
    try:
        return _MAPPING[domain_exception.exception_code]
    except KeyError:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
