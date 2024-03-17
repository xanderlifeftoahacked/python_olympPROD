from typing import Optional

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import JSON, Column, Integer, String, Boolean

engine = create_async_engine('sqlite+aiosqlite:///db/database.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class UserTable(Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    age = Column(Integer, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    travels = Column(JSON, nullable=True)


class TravelTable(Model):
    __tablename__ = 'travels'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    locations = Column(JSON, nullable=True)
    friends = Column(JSON, nullable=True)
    is_data_private = Column(Boolean, nullable=True, default=False)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
