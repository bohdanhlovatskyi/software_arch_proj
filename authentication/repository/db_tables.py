from .db import Base
from sqlalchemy import Column, Integer, String

class UserDataBase(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(40), unique=True, nullable=False)
    password = Column(String(80))


