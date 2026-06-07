import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.core.log import logger
from app.db.base import Base
from app.db.session import engine

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.web.parser import get_jobs
from telegram_bot.bot import dp, bot


scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(_: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    scheduler.add_job(
        get_jobs,
        trigger=IntervalTrigger(minutes=1),
        id='get_vacancies',
        replace_existing=True,
    )

    scheduler.start()
    bot_task = asyncio.create_task(dp.start_polling(bot))
    logger.info("Started")

    try:
        yield
    finally:
        logger.info("Finished")
        bot_task.cancel()
        await asyncio.gather(
            bot_task,
            return_exceptions=True,
        )
        await bot.session.close()
        scheduler.shutdown(wait=False)
        await engine.dispose()