from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt
from typing import Annotated

from db.pg.pg_worcker import pg_worcker_db
from models.models import Users, Match, UserAddress
from config import settings
from schemas.auth_schemas import Token, UserRegistration, TokenData
from exeptions.auth_exeptions import invalid_token, user_alredy_exist, credentials_exception, user_not_found, access_token_already_expired

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/clients/login")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict):
    to_encode = data.copy()
    token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + token_expires
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITM)
    return encoded_jwt


def get_jwt(data: dict) -> Token:
    access_token = create_token(data)
    refresh_token = create_token(data)
    token_type = 'bearer'
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=token_type
    )


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, settings.ALGORITM)


async def authenticate_user(login: str, password: str):
    user: Users = await pg_worcker_db.get_data(
        model=Users,
        filter_field='login',
        filter_value=login
    )
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def registrate_user(user_registrated: UserRegistration):
    hashed_password = get_password_hash(user_registrated.password)
    tokens: Token = get_jwt(data={'sub': user_registrated.login})
    user_registrated.password = hashed_password
    delattr(user_registrated, 'password')
    user = await pg_worcker_db.set_data(
        model=Users,
        hashed_password=hashed_password,
        refresh_token=tokens.refresh_token,
        ** user_registrated.dict()
    )
    if not user:
        raise user_alredy_exist
    return tokens


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Users:
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

    except InvalidTokenError:
        raise access_token_already_expired
    user = await pg_worcker_db.get_data(
        model=Users,
        filter_field='login',
        filter_value=username)
    if not user:
        raise user_not_found
    return user
