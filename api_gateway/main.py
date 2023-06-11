from fastapi import FastAPI, status

import controller

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['api_gateway'], 
    prefix='/api_gateway'
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}

# TO RUN:
# uvicorn main:app --host 0.0.0.0 --port 8000