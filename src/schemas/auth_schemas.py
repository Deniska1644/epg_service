from pydantic import BaseModel, EmailStr, field_validator
from fastapi import Form, UploadFile
from typing import List, Dict
from datetime import datetime

from exeptions.validation_exeption import user_sex_exeption
from models.models import Users


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
    sex: str = Form(...)
    email: EmailStr = Form(...)
    password: str = Form(...)
    name: str = Form(...)
    last_name: str = Form(...)
    file: UploadFile | None | str = Form(None)

    @field_validator('sex')
    @classmethod
    def chec_sex(cls, v: str) -> str:
        if v is not None:
            if v.lower().strip() not in ['male', 'femail']:
                raise user_sex_exeption
            return v.lower().strip()
        return v


class UserRead(BaseModel):
    id: int
    name: str
    last_name: str
    sex: str
    date_registration: datetime


# class ListUsers(BaseModel):
#     users: Dict[str,UserRead]
