from db.pg.pg_worcker import pagination
from schemas.app_schemas import UserFilter
from schemas.auth_schemas import UserRead

from typing import List
from models.models import Users


async def get_list_user(filters: UserFilter):
    result: List[Users] = await pagination.get_users(filters=filters)
    user_list_filter = []
    if result:
        for user in result:
            user_ = UserRead(
                id=user.id,
                name=user.name,
                last_name=user.last_name,
                sex=user.sex,
                date_registration=user.date_registration
            )
            user_list_filter.append(user_)

        return user_list_filter
    return user_list_filter
