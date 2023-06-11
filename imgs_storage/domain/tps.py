from pydantic import BaseModel


class ImageMetadata(BaseModel):
    user_id: str
    image_id: str
    img_name: str
    img_description: str

class ImageId(BaseModel):
    user_id: str
    img_id: str
