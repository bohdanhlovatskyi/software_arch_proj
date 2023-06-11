

from typing import List
from pydantic import BaseModel

class Embedding(BaseModel):
    type: str
    body: List[float]
