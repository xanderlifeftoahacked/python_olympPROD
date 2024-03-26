from sqlalchemy import Column, select

import db


class UserRepository:
    @classmethod
    async def add_one(cls, data: dict) -> Column[int]:
        async with db.new_session() as session:
            valid_data = {key: value for key, value in data.items(
            ) if key in db.UserTable.__table__.columns.keys()}
            user = db.UserTable(**valid_data)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id

    @classmethod
    async def id_exists(cls, user_id: int) -> bool:
        async with db.new_session() as session:
            user = await session.get(db.UserTable, user_id)
            if user:
                return True
            else:
                return False

    @classmethod
    async def select_by_id(cls, id: int) -> dict:
        async with db.new_session() as session:
            user = await session.get(db.UserTable, id)
            if not user:
                return {}
            return user.__dict__

    @classmethod
    async def update_by_id(cls, user_id: int, data: dict) -> None:
        async with db.new_session() as session:
            user = await session.get(db.UserTable, user_id)
            if user:
                for key, value in data.items():
                    setattr(user, key, value)
                await session.flush()
                await session.commit()
            else:
                raise ValueError(f"User with ID {user_id} not found.")


class TravelRepository:
    @classmethod
    async def add_one(cls, data: dict) -> Column[int]:
        async with db.new_session() as session:
            valid_data = {key: value for key, value in data.items(
            ) if key in db.TravelTable.__table__.columns.keys()}
            travel = db.TravelTable(**valid_data)
            session.add(travel)
            await session.flush()
            await session.commit()
            return travel.id

    @classmethod
    async def select_by_id(cls, id: int) -> dict:
        async with db.new_session() as session:
            travel = await session.get(db.TravelTable, id)
            if not travel:
                return {}
            return travel.__dict__

    @classmethod
    async def remove_by_id(cls, id: int) -> dict:
        async with db.new_session() as session:
            travel = await session.get(db.TravelTable, id)
            if travel:
                await session.delete(travel)
                await session.flush()
                await session.commit()
                return travel.__dict__
            return {}

    @classmethod
    async def update_by_id(cls, id: int, data: dict) -> None:
        async with db.new_session() as session:
            travel = await session.get(db.TravelTable, id)
            if travel:
                for key, value in data.items():
                    setattr(travel, key, value)
                await session.flush()
                await session.commit()
            else:
                raise ValueError(f"Travel with id {id} not found.")

    @classmethod
    async def name_exists(cls, name: str, owner: int) -> bool:
        async with db.new_session() as session:
            travel = await session.execute(select(db.TravelTable).where(
                db.TravelTable.name == name, db.TravelTable.owner == owner))
            if travel.scalar():
                return True
            else:
                return False
