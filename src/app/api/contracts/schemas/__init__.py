from abc import ABC

from app.application.contracts.use_cases.use_case_contract import UseCaseContract


class Handler(ABC):
    def __init__(self, use_case: UseCaseContract, http_request) -> None: