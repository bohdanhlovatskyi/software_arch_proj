from fastapi import (
    APIRouter, 
)

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from domain.userinfo import UserInfo
from domain.jwt import TokenResponse, TokenUser
from service.jwt import create_access_token, get_data_from_access_token
from service.auth import register, login



router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")

@router.post('/register')
def user_registration(user: UserInfo):
    return register(user)


@router.post('/login')
def user_login(payload: UserInfo):
    return login(payload)


@router.post('/create', response_model=TokenResponse)
async def create_toke(payload: TokenUser):
    access_token = create_access_token(
        data={"id": payload.id, "email": payload.email}
    )
    return {"token": access_token, "status": "success"}

@router.get('/decode', response_model=TokenUser)
def get_data_from_token(access_token: str = Depends(oauth2_scheme)):
    return get_data_from_access_token(access_token)