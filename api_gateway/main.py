from fastapi import FastAPI, status

from fastapi.middleware.cors import CORSMiddleware
import controller

origins = [
    "http://localhost:3000"
]

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['api_gateway'], 
    prefix='/api_gateway'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}

# TO RUN:
# uvicorn main:app --host 0.0.0.0 --port 8000