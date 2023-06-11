from fastapi import (
    APIRouter, 
    UploadFile, 
    Form, 
    File
)
import requests
import uuid

router = APIRouter()


STORAGE_URL="http://localhost:8000/"
PROCESSING_URL="http://localhost:8000/"


@router.post('/upload')
async def upload_image(file: UploadFile = File(...), name: str = Form(...), description: str = Form(...)):
    content = await file.read()

    json_data = {
        "user_id": str(uuid.uuid4()),
        "image_id": str(uuid.uuid4()),
        "img_name": name,
        "img_description": description
    }
    print(json_data)

    headers = {
        "Content-Type": "multipart/form-data"
    }

    files = {
        "file": content
    }

    response = requests.post(STORAGE_URL, data=json_data, files=files, headers=headers)

    if response.status_code == 200:
        print("Request successful")
    else:
        print("Request failed:", response.text)


@router.post("/query")
async def receive_text(text: str = Form(...)):
    json_data = {
        "user_id": str(uuid.uuid4()),
        "image_id": str(uuid.uuid4()),
        "query_text": text
    }
    print(json_data)

    response = requests.post(PROCESSING_URL, data=json_data)

    if response.status_code == 200:
        print("Request successful")
    else:
        print("Request failed:", response.text)