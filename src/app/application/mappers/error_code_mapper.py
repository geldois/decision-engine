from app.application.errors.error_code import ErrorCode
from app.domain.exceptions.decision_exception import DecisionException
from app.domain.exceptions.domain_exception import DomainException
from app.domain.exceptions.event_exception import EventException
from app.domain.exceptions.rule_exception import RuleException

_MAPPING: dict[type[DomainException], ErrorCode] = {
    DecisionException: ErrorCode.INVALID_DECISION,
    EventException: ErrorCode.INVALID_EVENT,
    RuleException: ErrorCode.INVALID_RULE,
}


def map_domain_exception_to_error_code(
    domain_exception: type[DomainException],
) -> ErrorCode:
    return _MAPPING[domain_exception]


def map_error_code_to_domain_exception(
    error_code: ErrorCode,
) -> type[DomainException] | None:
    for domain_exception, error in _MAPPING.items():
        if error is error_code:
            return domain_exception
