import asyncio
from sqlalchemy import select, insert, delete, update, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type, Dict


from db.connect import DbConnect
from config import settings
from models.models import Users
from schemas.app_schemas import UserFilter


class PgWorckerBase(DbConnect):

    async def set_data(self,  model: Type[DeclarativeMeta], **kwargs):
        async with self.async_session_maker() as session:
            if not kwargs:
                raise ValueError(f'{self.__name__} ожидает kwargs')
            try:
                query = insert(model).values(**kwargs)
                res = await session.execute(query)
                await session.commit()
                return res
            except Exception as e:
                print(f"{e}")
                await self.rollback()
                return None

    async def get_data(self, model: Type[DeclarativeMeta], filter_field: str, filter_value: str):
        async with self.async_session_maker() as session:
            try:
                query = select(model).where(
                    getattr(model, filter_field) == filter_value)
                res = await session.execute(query)
                data = res.scalars().first()
                return data

            except Exception as e:
                print(f"{e}")
                return None

    async def update_data(self,  model: Type[DeclarativeMeta], filter_field: str, filter_value: str, **kwargs):
        async with self.async_session_maker() as session:
            try:
                query = update(model).where(
                    getattr(model, filter_field) == filter_value).values(**kwargs)
                res = await session.execute(query)
                await session.commit()
                return res

            except Exception as e:
                print(f"{e}")
                await self.rollback()
                return None

    async def delete_data(self,  model: Type[DeclarativeMeta], filter_field: str, filter_value: str):
        async with self.async_session_maker() as session:
            try:
                query = delete(model).where(
                    getattr(model, filter_field) == filter_value)
                res = await session.execute(query)
                await session.commit()
                return res
            except Exception as e:
                print(f"{e}")
                await self.rollback()
                return None


class UserPaginator(PgWorckerBase):
    async def get_users(self, filters: UserFilter = None, start: int = 0, stap: int = 10):
        async with self.async_session_maker() as session:
            try:
                filters_query = []

                for key, value in filters.dict().items():
                    if value is not None:
                        if key == 'date_registration_from':
                            filters_query.append(
                                Users.date_registration >= filters.date_registration_from)
                        elif key == 'date_registration_to':
                            filters_query.append(
                                Users.date_registration <= filters.date_registration_to)
                        else:
                            filters_query.append(
                                (getattr(Users, key) == value))
                query = select(Users).where(
                    and_(
                        *filters_query
                    )
                )
                res = await session.execute(query)
                data = res.scalars().all()
                return data
            except Exception as e:
                print(f"{e}")
                return None


pg_worcker_db = PgWorckerBase(settings.pg_url())
pagination = UserPaginator(settings.pg_url())
