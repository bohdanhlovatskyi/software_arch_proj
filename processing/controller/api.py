import numpy as np
from fastapi import (
    APIRouter, 
)

from domain import Message, Embedding
from service import process_entry

from typing import Dict, List

router = APIRouter()

@router.post('/', status_code=200)
def post_processsing_entry(entry: Dict[str, str]) -> Embedding:
    msg = Message(type=entry["type"], body=entry["body"])
    print("received for processing: ", msg)
    return process_entry(msg)
