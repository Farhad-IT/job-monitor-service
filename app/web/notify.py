from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import AsyncSessionLocal
from app.subscription.models import SubscriptionModel
from app.vacancies.models import VacancyModel
from telegram_bot.bot import bot


async def notify_users(vacancy: VacancyModel):
    async with AsyncSessionLocal() as session:
        res = await session.scalars(
            select(SubscriptionModel)
            .options(selectinload(SubscriptionModel.user))
        )
        subscriptions = res.all()

        for sub in subscriptions:
            chek_sub = (
                sub.keyword.lower() in vacancy.company.lower() or
                sub.keyword.lower() in vacancy.title.lower()
            )

            if not chek_sub:
                continue

            if chek_sub:
                await bot.send_message(
                    sub.user.telegram_id,
                    (
                        f"Новая вакансия найдена по подписке: {sub.keyword}\n"
                        f"🚀 {vacancy.title}\n"
                        f"🏢 {vacancy.company}\n"
                        f"📍 {vacancy.location}\n"
                        f"🔗 {vacancy.url}"
                    )
                )