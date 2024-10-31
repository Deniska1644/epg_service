from fastapi import APIRouter, Depends, Query
from typing import Optional, Annotated
from enum import Enum

from auth.depends import get_current_user
from schemas.auth_schemas import UserLogin
from schemas.app_schemas import UserFilter
from dateapp.depends import get_list_user

router = APIRouter(
    prefix=''
)


class SexEnum(str, Enum):
    male = "male"
    female = "female"


@router.get('/list')
async def main(
    filter: UserFilter = Depends()
):
    res = await get_list_user(filter)
    return {'smf': res}
