from fastapi import (
    APIRouter, 
    UploadFile, 
    Form, 
    File,
    Response
)
import requests
import uuid
import json
import base64

router = APIRouter()

STORAGE_URL_UPLOAD='http://localhost:9020/imgs_storage/upload/'
ENGINE_URL="http://localhost:8000/"
PROCESSING_URL="http://localhost:8000/"


@router.post('/upload')
async def upload_image(file: UploadFile = File(...), name: str = Form(...), description: str = Form(...)):
    content = await file.read()

    payload = {
        "user_id": '1',
        "img_name": name,
        "img_description": description,            
        'image': base64.b64encode(content).decode('utf-8')
    }

    json_payload = json.dumps(payload)

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(STORAGE_URL_UPLOAD, data=json_payload, headers=headers)

    


@router.post("/query")
async def receive_text(text: str = Form(...)):
    processing_json = {
        "type": "text",
        "body": text
    }
    print(processing_json)

    # response = requests.post(PROCESSING_URL, data=processing_json)

    # embedding = response.json().body

    # # TODO: get correct user id
    # user_id = str(uuid.uuid4())

    # engine_json = {
    #     "user_id": user_id,
    #     "body": embedding
    # }
    # response = requests.post(ENGINE_URL, data=engine_json)

    # idxs = response.json().documents

    # storage_json = {
    #     "user_id": user_id,
    #     "image_idxs": idxs
    # }
    # response = requests.post(STORAGE_URL, data=storage_json)

    # image_data = response.image_data

    with open("Yaroslav.jpg", "rb") as file:
        image_data = file.read()

    headers = {
        "Content-Type": "image/jpeg"
    }

    return Response(content=image_data, headers=headers)
