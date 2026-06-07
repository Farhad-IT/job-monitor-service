from sqlalchemy import select, Sequence, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.subscription.models import SubscriptionModel


class SubscribeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_subscriptions(self, user_id: int) -> Sequence[SubscriptionModel]:
        subscriptions = select(SubscriptionModel).where(SubscriptionModel.user_id == user_id)
        result = await self.db.execute(subscriptions)
        return result.scalars().all()

    async def create_subscription(self, user_id: int, keyword: str) -> SubscriptionModel:
        subscription = SubscriptionModel(user_id=user_id, keyword=keyword)
        self.db.add(subscription)
        return subscription

    async def delete_subscription(self, subscription_id: int, user_id: int) -> None:
        await self.db.execute(
            delete(SubscriptionModel)
            .filter(
                SubscriptionModel.id == subscription_id,
                SubscriptionModel.user_id == user_id
            )
        )