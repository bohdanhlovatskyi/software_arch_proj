from fastapi import (
    APIRouter, 
)

from domain import EmbeddingEntry
from service import save_image, find_closest

from typing import Dict, List

router = APIRouter()

# TODO: is it ok to return str? 
@router.post('/save', status_code=200)
def save_img_embedding(entry: Dict) -> str:
    emb = EmbeddingEntry(
        user_id=entry["user_id"], 
        img_id=entry["image_id"], 
        body=entry["body"], 
    )
    
    return save_image(emb)

@router.post('/query', status_code=200)
def get_closest(entry: Dict):
    emb = EmbeddingEntry(
        user_id=entry["user_id"],
        body=entry["body"],
        img_id="", 
    )

    return find_closest(emb)
