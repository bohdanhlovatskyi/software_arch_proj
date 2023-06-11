import json
import sys
sys.stdout.flush()

from uuid import uuid4 as get_uuid
import aiohttp
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from service import save_img, get_img
from domain import ImageMetadata


# logger = Logger('/logs/minio_manager.txt', 'MINIO_MANAGER')

router = APIRouter()


@router.post('/upload')
async def upload_image(file: UploadFile = File(...), meta: ImageMetadata = Form(...)):
    content = await file.read()

    try:
        img = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Failed to read file: {e}')
    print(f'Item: {meta}')
    return 'OK'

    res = save_img(img, data_dict)
    return res

@router.get("/")
async def get_messages() -> str:
    return 'OK'
