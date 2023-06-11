import os
import io

import json

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
            print(f'bucket "{self.bucket_name} already exists')
    
    def save_img_to_s3(self, img: bytes, data_dict: dict):
        f_ext = data_dict['img_name'].split('.')[-1]
        f_path = os.path.join(data_dict["user_id"], f'{data_dict["image_id"]}.{f_ext}')

        print(f'file path S3: {f_path}')
        data = io.BytesIO(img)
        size = len(data.getbuffer())
        self.minio_client.put_object(self.bucket_name, f_path, data, size)
        return  {'status': 'OK', 'f_path': f_path, 'size': size}

    def get_img(self):
        pass

manager_S3 = ManagerS3()
