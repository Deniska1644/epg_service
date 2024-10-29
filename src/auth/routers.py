from fastapi import APIRouter, File, UploadFile, Body
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated, Optional

from schemas.auth_schemas import Token, UserRegistration
from auth.depends import authenticate_user, get_jwt, registrate_user
from exeptions.auth_exeptions import incorrect_username_or_password


router = APIRouter(
    prefix='/clients'
)


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise incorrect_username_or_password
    tokens: Token = get_jwt(data={"sub": form_data.username})
    return tokens


@router.post('/create', response_model=UserRegistration)
async def register_user(
    user_data: UserRegistration = Body(...),
    file: Optional[UploadFile] = File(None)
):
    tokens = await registrate_user(user_data)
    if file:
        # Обработка файла (например, сохранение)
        with open(file.filename, "wb") as f:
            content = await file.read()
            f.write(content)
        tokens['photo_filename'] = file.filename  # Добавляем имя файла в ответ
    return tokens
