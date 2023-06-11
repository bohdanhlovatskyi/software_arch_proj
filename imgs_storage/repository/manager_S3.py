import os
import io

import json
import base64

from typing import List
from minio import Minio
from minio.error import S3Error

class ManagerS3:
    def __init__(self) -> None:
        credentials_path = 'credentials.json'
        with open(credentials_path, 'r') as f:
            credentials = json.loads(f.read())

        minio_url = 'minio:9000'
        minio_access_key = credentials['accessKey']
        minio_secret_key = credentials['secretKey']

        self.bucket_name = 'imgs'
        self.minio_client = Minio(
            endpoint=minio_url,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False,
        )
        if not self.minio_client.bucket_exists(self.bucket_name):
            print(f'creating bucket, name: "{self.bucket_name}"')
            self.minio_client.make_bucket(self.bucket_name)
        else:
            print(f'bucket "{self.bucket_name}" already exists')
    
    def save_img_to_s3(self, img: bytes, path_s3: str):
        print(f'file path S3: {path_s3}')
        data = base64.b64decode(img)
        data = io.BytesIO(data)
        size = len(data.getbuffer())
        self.minio_client.put_object(self.bucket_name, path_s3, data, size)
        return  {'status': 'OK', 'f_path': path_s3, 'size': size}

    def get_img(self):
        pass

manager_S3 = ManagerS3()
