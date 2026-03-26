from app.application.errors.application_error import ApplicationError
from app.domain.exceptions.domain_exception import DomainException


def map_domain_exception_to_application_error(
    domain_exception: DomainException,
) -> ApplicationError:
    return ApplicationError(domain_exception)


def map_application_error_to_domain_exception(
    application_error: ApplicationError,
) -> type[DomainException]:
    return application_error.value
