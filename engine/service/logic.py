import ast

from domain import EmbeddingEntry
from repository import storage

from configparser import ConfigParser
from confluent_kafka import Producer, Consumer

config_parser = ConfigParser(interpolation=None)

with open('config.properties', 'r') as config_file:
    config_parser.read_file(config_file)

producer_config = dict(config_parser['kafka_client'])
consumer_config = dict(config_parser['kafka_client'])
consumer_config.update(config_parser['consumer'])

def save_image(entry: EmbeddingEntry) -> str:
    storage.add_image_embedding(
        client=entry.user_id, 
        img_id=entry.img_id, 
        img_embedding=entry.body
    )

    return "OK"

def find_closest(entry: EmbeddingEntry):    
    res = storage.query(
        client=entry.user_id, 
        embedding=entry.body
    )

    return res

def consume_embeddings():
    embedding_consumer = Consumer(consumer_config)
    embedding_consumer.subscribe(["embedding"])

    while True:
        event = embedding_consumer.poll(1.)
        if event is None:
            continue

        if event.error():
            print("engine: error", event.error())
            continue

        entry = ast.literal_eval(event.value().decode("utf-8"))

        try:
            entry = EmbeddingEntry(
                user_id=entry["user_id"], 
                img_id=entry["img_id"], 
                body=entry["body"], 
            )
            status = save_image(entry)
        except Exception as ex:
            print(ex)
            continue

        print(f"saving image: {entry.img_id} for {entry.user_id}", status)

        # TODO: add error notication to error service
