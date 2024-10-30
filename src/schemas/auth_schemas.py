from pydantic import BaseModel
from pydantic import EmailStr, field_validator
from fastapi import Form, UploadFile


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserLogin(BaseModel):
    login: str
    password: str
    refresh_token: str


class TokenData(BaseModel):
    username: str | None = None


class UserRegistration(BaseModel):
    login: str = Form(...)
    email: EmailStr = Form(...)
    password: str = Form(...)
    name: str = Form(...)
    last_name: str = Form(...)
    file: UploadFile | None = Form(None)

    # @field_validator('email')
    # @classmethod
    # def email_validatir(cls, v):
