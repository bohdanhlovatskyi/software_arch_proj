
from domain import EmbeddingEntry
from repository import storage

def save_image(entry: EmbeddingEntry) -> str:
    storage.add_image_embedding(
        client=entry.user_id, 
        img_id=entry.img_id, 
        img_embedding=entry.body
    )

    return "OK"

def find_closest(entry: EmbeddingEntry):    
    res = storage.query(
        client=entry.user_id, 
        embedding=entry.body
    )

    return res
