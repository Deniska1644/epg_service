import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import IntegrityError
from typing import AsyncGenerator

from config import settings


class DbConnect:

    def __init__(self, database: str):
        self.DATABASE_URL = database
        self.engine = create_async_engine(self.DATABASE_URL)
        self.async_session_maker = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False)
        self.session = None

    async def create_session(self) -> None:
        self.session = await self.async_session_maker()

    async def close_session(self) -> None:
        if self.session:
            await self.session.close()
            self.session = None

    async def commit(self) -> None:
        if self.session:
            await self.session.commit()

    async def rollback(self) -> None:
        if self.session:
            await self.session.rollback()
