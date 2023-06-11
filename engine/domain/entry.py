from typing import List
from pydantic import BaseModel

class EmbeddingEntry(BaseModel):
    user_id: str
    body: List[float]
    img_id: str
