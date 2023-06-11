

from typing import List
from pydantic import BaseModel

class Embedding(BaseModel):
    type: str
    body: List[float]

class EmbeddingEntry(BaseModel):
    user_id: str
    body: List[float]
    img_id: str
