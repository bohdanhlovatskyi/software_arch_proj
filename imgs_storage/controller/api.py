import json
import sys
sys.stdout.flush()

from uuid import uuid4 as get_uuid
import aiohttp
from fastapi import APIRouter, Request
from service import save_img, get_img
from domain import ImageMetadata



router = APIRouter()


@router.post('/upload')
async def upload_image(request: Request):
    json_data = await request.json()
    res = save_img(json_data)
    return res

@router.get("/")
async def get_messages() -> str:
    return 'OK'
