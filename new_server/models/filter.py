from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class FilterOpEnum(StrEnum):
    lk = "like"
    eq = "=="
    ne = "!="
    gt = ">"
    lt = "<"
    ge = ">="
    le = "<="
class PaginationModel(BaseModel):
    limit: int | None = None
    offset: int | None = None

class LogicalOpEnum(StrEnum):
    AND = "AND"
    OR = "OR"
    NONE = "NONE"

class FilterModel(BaseModel):
    field: str
    op: FilterOpEnum
    value: Any

    def __repr__(self) -> str:
        return f"{self.field} {self.op} {self.value}"

class FilterGroup(BaseModel):
    log_op: LogicalOpEnum
    filters: list[FilterModel] = Field(default_factory=list)

class QueryParamsModel(PaginationModel):
    #filters: list[FilterModel] = Field(default_factory=list)
    filter_groups: list[FilterGroup] = Field(default_factory=list)