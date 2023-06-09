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

model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id)
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)

@torch.no_grad()
def process_image(image: PIL.Image) -> np.ndarray:
    image = processor(
        text=None,
        images=image,
        return_tensors="pt",
        padding=True
    )["pixel_values"]

    img_emb = model.get_image_features(image)

    return img_emb.numpy()

@torch.no_grad()
def process_text(query_sentecne: str) -> np.ndarray:
    inputs = tokenizer(query_sentecne, return_tensors="pt")
    text_emb = model.get_text_features(**inputs)

    return text_emb

if __name__ == "__main__":

    import pickle
    image = Image.open("cat.jpg")
    img_emb = process_image(image)

    text_emb = process_text("cat photo")
    with open("text_emb.pkl", "wb") as h:
        pickle.dump(text_emb, h)

    text_emb_dog = process_text("airplane")

    score = np.dot(text_emb, img_emb.T)
    print(score)

    score = np.dot(text_emb_dog, img_emb.T)
    print(score)
