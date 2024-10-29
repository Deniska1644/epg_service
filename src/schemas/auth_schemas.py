from pydantic import BaseModel
from pydantic import EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserLogin(BaseModel):
    login: str
    password: str
    refresh_token: str


class UserRegistration(BaseModel):
    login: str
    email: EmailStr
    password: str
    name: str
    last_name: str


class TokenData(BaseModel):
    username: str | None = None
