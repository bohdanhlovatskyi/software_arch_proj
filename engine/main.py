
from fastapi import FastAPI, status

import controller

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['engine'], 
    prefix='/engine'
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}