from typing import List, Optional

from pydantic import BaseModel, conint


PositiveInt = conint(gt=0)


class SequenceRequest(BaseModel):
    start: PositiveInt
    max_steps: Optional[PositiveInt] = None


class SequenceResponse(BaseModel):
    start: int
    iterations: int
    reached_one: bool
    last_value: int
    sequence: List[int]


class ScanRequest(BaseModel):
    start: PositiveInt
    count: PositiveInt
    max_steps: Optional[PositiveInt] = None


class ScanItem(BaseModel):
    start: int
    iterations: int
    reached_one: bool
    last_value: int


class ScanResponse(BaseModel):
    data: List[ScanItem]
