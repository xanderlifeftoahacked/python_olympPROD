from sqlalchemy import Column, select

import db


class UserRepository:
    @classmethod
    async def add_one(cls, data: dict) -> Column[int]:
        async with db.new_session() as session:
            user = db.UserTable(**data)
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
    async def select_by_id(cls, id: int) -> dict | None:
        async with db.new_session() as session:
            user = await session.get(db.UserTable, id)
            if not user:
                return None
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
