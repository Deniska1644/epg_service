import asyncio
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import Type


from db.connect import DbConnect
from config import settings
from models.models import Users


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
                await self.rollback()
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


pg_worcker_db = PgWorckerBase(settings.pg_url())
