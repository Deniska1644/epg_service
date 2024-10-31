from fastapi import APIRouter
from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated


from schemas.auth_schemas import Token, UserRegistration
from auth.depends import authenticate_user, get_jwt, registrate_user
from exeptions.auth_exeptions import incorrect_username_or_password
from utils.watermark.watermark_creater import image_worker


router = APIRouter(
    prefix='/auth'
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


@router.post('/create')
async def register_user(
    user_data: UserRegistration = Depends()
):
    if not user_data.file:
        tokens = await registrate_user(user_data)
        return tokens
    photo_path = await image_worker.save_image(user_data)
    image_worker.watermark_image(photo_path)
    tokens = await registrate_user(user_data, str(photo_path))
    return tokens
