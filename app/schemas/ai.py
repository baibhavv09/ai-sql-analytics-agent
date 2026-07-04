from pydantic import BaseModel
from typing import Any


class AIQueryResponse(BaseModel):
    success: bool
    result: Any