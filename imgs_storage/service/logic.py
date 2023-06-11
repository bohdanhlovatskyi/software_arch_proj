import os
from repository import manager_S3, cassandra_manager
from domain import ImageMetadata
from uuid import uuid4 as get_uuid

def save_img(json_data: dict) -> str:
    # img_id = str(get_uuid())
    img_id = '22'

    f_ext = json_data['img_name'].split('.')[-1]
    path_s3 = os.path.join(json_data["user_id"], f'{img_id}.{f_ext}')

    res = manager_S3.save_img_to_s3(json_data['image'], path_s3)
    cassandra_manager.insert_image_info(
        table_name="image_metadata", 
        user_id = json_data['user_id'],
        img_id = img_id,
        img_path = path_s3,
        img_description = json_data['img_description']
    )

    return res

def get_img_s3(user_id, img_id):
    img, url = manager_S3.get_img(user_id, img_id)
    return img, url
