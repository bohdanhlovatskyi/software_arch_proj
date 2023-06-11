from pydantic import BaseModel


class ImageMetadata(BaseModel):
    user_id: str
    img_id: str
    img_path: str
    img_description: str

class ImageId(BaseModel):
    user_id: str
    img_id: str
