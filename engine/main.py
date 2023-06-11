from threading import Thread
from fastapi import FastAPI, status

import controller
from service import consume_embeddings

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['engine'], 
    prefix='/engine'
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}

@app.on_event("startup")
def launch_background_consumer():
    t = Thread(target=consume_embeddings)
    t.start()
