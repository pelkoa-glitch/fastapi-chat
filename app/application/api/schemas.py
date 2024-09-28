from typing import (
    Generic,
    TypeVar,
)

from pydantic import BaseModel


class ErrorSchema(BaseModel):
    error: str


IT = TypeVar('IT', bound=BaseModel)


class BaseQueryResponseSchema(BaseModel, Generic[IT]):
    count: int
    offset: int
    limit: int
    items: IT
