from db.pg.pg_worcker import pagination, pg_worcker_db
# from config import settings
# from models.models import Users
from schemas.app_schemas import UserFilter
from schemas.auth_schemas import UserRegistration
from models.models import Users
import asyncio
import random


async def main():
    models = []
    pool = ['male', 'feemale']

    for i in range(1, 11):
        for y in range(1, 6):
            models.append(UserRegistration(
                login=f'name{i}{y}',
                sex=random.choice(pool),
                email=f'email{i}{y}@mail.ru',
                hashed_password='password',
                name=f'string{y}',
                last_name='lastname',
                photo=None
            ))

    for i,el in enumerate(models):
        await pg_worcker_db.set_data(model=Users, refresh_token=f'sdafsdf{i}', ** el.dict())
        print('ok')

asyncio.run(main())

# # async def main():
# #     pg = PgWorckerBase(settings.pg_url())
# #     a = await pg.set_data(
# #         model=Users,
# #         name='Den',
# #         login='deniska',
# #         last_name='Dens',
# #         email='email222',

# #     )
# #     # b = await pg.get_data(
#     #     model=Users,
#     #     filter_field='id',
#     #     filter_value=1
#     # )
#     # c = await pg.update_data(
#     #     model=Users,
#     #     filter_field='id',
#     #     filter_value=1,
#     #     name='dima'
#     # )

#     # d = await pg.delete_data(
#     #     model=Users,
#     #     filter_field='name',
#     #     filter_value='Den',
#     # )
#     # print(a, b, c, d)


# if __name__ == '__main__':
#     asyncio.run(main())
