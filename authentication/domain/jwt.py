from pydantic import BaseModel


class TokenUser(BaseModel):
    email: str
    id: int


class TokenResponse(BaseModel):
    status: str
    token: str