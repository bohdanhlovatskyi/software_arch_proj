from fastapi import FastAPI
from pydantic import BaseModel
from repository import CassandraClient


service = FastAPI()

host = "localhost"
port = 9042
keyspace = "software_arch_proj"
client = CassandraClient(host, port, keyspace)
client.connect()


class ImageMetadata(BaseModel):
    user_id: str
    img_id: str
    img_path: str
    img_description: str

class ImageId(BaseModel):
    user_id: str
    img_id: str


@service.post("/")
async def root(image_data: ImageMetadata):
    print(image_data)
    client.insert_image_info(table_name="image_metadata", 
                             user_id=image_data.user_id,
                             img_id=image_data.img_id,
                             img_path=image_data.img_path,
                             img_description=image_data.img_description)
    
@service.get("/")
async def root(image_id: ImageId):
    print(image_id)
    rows = client.get_image_info(table_name="image_metadata", 
                                 user_id=image_id.user_id,
                                 img_id=image_id.img_id)
    rows = list(list(rows)[0])
    image_description, image_data = rows
    print(f"image description: {image_description}, image_name: {image_data}")

# TO RUN:
# uvicorn example_write:service --host 0.0.0.0 --port 8000

# POST:
# curl -d '{"user_id":"1", "img_id":"1", "img_path":"hello.jpg", "img_description":"my_image"}' -H "Content-Type: application/json" -X POST http://localhost:8000/
# curl -d '{"user_id":"2", "img_id":"2", "img_path":"hello.jpg", "img_description":"my_image"}' -H "Content-Type: application/json" -X POST http://localhost:8000/

# GET:
# curl -d '{"user_id":"1", "img_id":"1"}' -H "Content-Type: application/json" -X GET http://localhost:8000/
# curl -d '{"user_id":"2", "img_id":"2"}' -H "Content-Type: application/json" -X GET http://localhost:8000/