import json
import sys
sys.stdout.flush()

from uuid import uuid4 as get_uuid
import aiohttp
from fastapi import APIRouter, Request
from service import save_img, get_img_s3
from domain import ImageMetadata



router = APIRouter()


@router.post('/upload')
async def upload_image(request: Request):
    json_data = await request.json()
    res = save_img(json_data)
    return res

@router.get("/load")
async def get_img(request: Request) -> str:
    json_data = await request.json()
    user_id = json_data['user_id'] 
    img_id = json_data['img_id'] 
    img, url = get_img_s3(user_id, img_id)
    with open('/out/1.png', 'wb') as file_data:
        for d in img.stream(32*1024):
            file_data.write(d)

    return 'OK'
