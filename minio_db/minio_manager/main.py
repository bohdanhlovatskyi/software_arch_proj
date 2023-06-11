from logger import Logger
import logging
import json
import io
import os
import sys
sys.stdout.flush()

from uuid import uuid4 as get_uuid
import aiohttp
from fastapi import FastAPI, UploadFile, File

from minio import Minio
from minio.error import S3Error

logger = Logger('/logs/minio_manager.txt', 'MINIO_MANAGER')

app = FastAPI()

credentials_path = 'credentials.json'
with open(credentials_path, 'r') as f:
    credentials = json.loads(f.read())

minio_url = 'minio:9000'
minio_access_key = credentials['accessKey']
minio_secret_key = credentials['secretKey']


logger.log(f'minio_url {minio_url}')
logger.log(f'minio_access_key {minio_access_key}')
logger.log(f'minio_secret_key {minio_secret_key}')

bucket_name = 'imgs'
logger.set_context(f'creating minio client')
minio_client = Minio(
    endpoint=minio_url,
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False,
)
if not minio_client.bucket_exists(bucket_name):
    logger.log(f'creating bucket, name: "{bucket_name}"')
    minio_client.make_bucket(bucket_name)
else:
    logger.log(f'bucket "{bucket_name} already exists')

@app.on_event("startup")
def startup_event():
    logger.set_context('startup')
    logger.reset_context()

@app.on_event("shutdown")
async def shutdown():
    logger.set_context('shutdown', msg='removing trash')
    logger.reset_context()

@app.post("/", status_code=201)
async def upload_img(image: UploadFile = File(...)):
    file_content = await image.read()
    image.close()

    uuid = get_uuid()
    f_name = image.filename
    f_name = os.path.basename(f_name)
    f_name = f'{uuid}_{f_name}'
    print(f'file name: {f_name}')

    data = io.BytesIO(file_content)
    size = len(data.getbuffer())

    # f_ext = os.path.splitext(image.filename)[1][1:]
    # logger.log(f'img_name: {image.filename}; img ext: {f_ext}, uuid: {uuid}')
    # img_url = f"{minio_url}/{bucket_name}/{f_name}"
    # logger.log(f'img url: {img_url}')

    # Upload the image to MinIO
    minio_client.put_object(bucket_name, f_name, data, size)

    logger.reset_context('Success')
    return {'filename': f_name, 'size': size}


@app.get("/")
async def get_messages() -> str:
    return 'OK'
