from fastapi import APIRouter

router = APIRouter()

@router.post('/save', status_code=200)
def save_img(image) -> str:
    return 

@router.post('/query', status_code=200)
def search_for_image(description: str):
    return
