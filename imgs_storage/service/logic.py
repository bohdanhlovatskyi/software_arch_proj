import os
from repository import manager_S3, cassandra_manager
from domain import ImageMetadata, ImageId
from uuid import uuid4 as get_uuid
from configparser import ConfigParser
from confluent_kafka import Producer
from kafka.admin import KafkaAdminClient, NewPartitions

admin_client = KafkaAdminClient(bootstrap_servers="kafka-server:9092")
topic_partitions = {}
topic_partitions["query"] = NewPartitions(total_count=1)
topic_partitions["embedding"] = NewPartitions(total_count=1)

config_parser = ConfigParser(interpolation=None)

with open('config.properties', 'r') as config_file:
    config_parser.read_file(config_file)
producer_config = dict(config_parser['kafka_client'])

image_producer = Producer(producer_config)

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

    entry = ImageId(
        user_id=json_data["user_id"], 
        img_id=json_data["img_id"],
    )
    
    image_producer.produce(
            'query', key=str(0), value=entry.json()
    )

    return res

def get_img_s3(user_id, img_id):
    img, url = manager_S3.get_img(user_id, img_id)
    return img, url
