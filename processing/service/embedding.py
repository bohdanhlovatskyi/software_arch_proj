
import PIL
import ast
import json
import torch
import requests
from PIL import Image
from transformers import (
    CLIPTokenizerFast,
    CLIPProcessor,
    CLIPModel
)

from typing import List
from domain import Message, Embedding, EmbeddingEntry

from configparser import ConfigParser
from confluent_kafka import Producer, Consumer

# TODO: better way would be some kind of registry and init in main
model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

config_parser = ConfigParser(interpolation=None)

with open('config.properties', 'r') as config_file:
    config_parser.read_file(config_file)

producer_config = dict(config_parser['kafka_client'])
consumer_config = dict(config_parser['kafka_client'])
consumer_config.update(config_parser['consumer'])

def process_entry(entry: Message) -> Embedding:
    # TODO: add enumeration for this
    if entry.type == "url":
        try:
            img_stream = requests.get(entry.body, stream=True).raw
        except Exception as ex:
            print(ex)
            return
        return Embedding(type=entry.type, body=process_image(Image.open(img_stream)))
    elif entry.type == "text":
        return Embedding(type=entry.type, body=process_text(entry.body))
    else:
        raise NotImplemented

@torch.no_grad()
def process_image(image: PIL.Image) -> List[float]:
    image = processor(
        text=None,
        images=image,
        return_tensors="pt",
        padding=True
    )["pixel_values"]

    img_emb = model.get_image_features(image)
    return list(img_emb.squeeze(0).numpy())

@torch.no_grad()
def process_text(query_sentence: str) -> List[float]:
    inputs = tokenizer(query_sentence, return_tensors="pt")
    text_emb = model.get_text_features(**inputs)
    return list(text_emb.squeeze(0).numpy())

def consume_orders():
    order_consumer = Consumer(consumer_config)
    order_consumer.subscribe(["query"])

    embedding_producer = Producer(producer_config)

    while True:
        event = order_consumer.poll(1.)
        if event is None:
            continue

        if event.error():
            print("processing: error", event.error())
            continue

        # TODO: should be decomposed into same processing as in controller
        try:
            entry = ast.literal_eval(event.value().decode("utf-8"))
            print("received: ", entry)
            msg_entry = Message(type="url", body=entry["body"])
            emb = process_entry(msg_entry)
            if emb is None:
                continue

            entry = EmbeddingEntry(
                user_id=entry["user_id"], 
                img_id=entry["img_id"], 
                body=emb.body, 
            )
        except Exception as ex: 
            print(ex)
            continue

        embedding_producer.produce(
            'embedding', key=str(0), value=entry.json()
        )
