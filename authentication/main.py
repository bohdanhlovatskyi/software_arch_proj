from fastapi import FastAPI, status

from controller import api 

app = FastAPI()
app.include_router(
    api.router, 
    tags=['authentication'], 
    prefix='/authentication'
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}
