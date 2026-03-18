from abc import ABC

from pydantic import BaseModel


class HttpContract(ABC, BaseModel):
    pass
