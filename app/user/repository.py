from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.user.models import UserModel


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_telegram_id(self, telegram_id: int) -> UserModel:
        user = select(UserModel).where(UserModel.telegram_id == telegram_id)
        result =  await self.db.execute(user)
        return result.scalar_one_or_none()

    async def create_user(self, telegram_id: int) -> UserModel:
        user = UserModel(telegram_id=telegram_id)
        self.db.add(user)
        return user