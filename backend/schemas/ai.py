from pydantic import BaseModel
from typing import Any


class AIQueryRequest(BaseModel):
    question: str


class AIQueryResponse(BaseModel):
    success: bool
    result: Any