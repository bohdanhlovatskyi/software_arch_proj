from pydantic import BaseModel

class UserInfo(BaseModel):
    login: str
    password: str
