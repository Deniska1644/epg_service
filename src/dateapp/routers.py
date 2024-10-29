from fastapi import APIRouter, Depends
from typing import Annotated

from auth.depends import get_current_user
from schemas.auth_schemas import UserLogin

router = APIRouter()


@router.get('/list')
async def main(
    current_user: Annotated[UserLogin, Depends(get_current_user)]
):
    return {'status': current_user.refresh_token}
