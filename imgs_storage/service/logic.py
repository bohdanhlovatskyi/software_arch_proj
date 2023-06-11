
from repository import manager_S3, cassandra_manager
from domain import ImageMetadata

def save_img(img: bytes, data_dict: dict, image_data: ImageMetadata) -> str:
    res = manager_S3.save_img_to_s3(img, data_dict)
    cassandra_manager.insert_image_info(table_name="image_metadata", 
                             user_id=image_data.user_id,
                             img_id=image_data.img_id,
                             img_path=image_data.img_path,
                             img_description=image_data.img_description)

    return res

def get_img(user_id, img_id):    
    res = 'OK'

    return res
