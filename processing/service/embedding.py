

import PIL
import torch
import requests
import numpy as np
from PIL import Image
from transformers import (
    CLIPTokenizerFast,
    CLIPProcessor,
    CLIPModel
)

from typing import List
from domain import Message, Embedding

# TODO: better way would be some kind of registry and init in main
model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

def process_entry(entry: Message) -> Embedding:
    # TODO: add enumeration for this
    if entry.type == "url":
        img_stream = requests.get(entry.body, stream=True).raw
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
