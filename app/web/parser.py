import asyncio

import httpx
from sqlalchemy.dialects.postgresql import insert

from app.web.notify import notify_users
from app.core.log import logger


from app.db.session import AsyncSessionLocal
from app.vacancies.models import VacancyModel



URL = "https://remoteok.com/api"


async def get_jobs():
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(URL)
        response.raise_for_status()
        data = response.json()

    jobs = data[1:]

    rows = []

    for job in jobs:
        external_id = job.get("id")

        if not external_id:
            continue

        rows.append(
            {
                "external_id": str(external_id),
                "company": job.get("company"),
                "title": job.get("position"),
                "location": job.get("location"),
                "url": job.get("url"),
            }
        )

    async with AsyncSessionLocal() as session:

        stmt = (
            insert(VacancyModel)
            .values(rows)
            .on_conflict_do_nothing(
                index_elements=["external_id"]
            )
            .returning(
                VacancyModel.external_id,
                VacancyModel.company,
                VacancyModel.title,
                VacancyModel.location,
                VacancyModel.url,
            )
        )

        result = await session.execute(stmt)

        inserted = result.mappings().all()

        await session.commit()

        if not inserted:
            logger.info("No new vacancies to add")
            return

        for row in inserted:
            logger.info(
                "New vacancy found: %s | %s (%s)",
                row["company"],
                row["title"],
                row["external_id"],
            )
            await notify_users(row)

        logger.info(
            "Added %s new vacancies",
            len(inserted),
        )


async def main():
    await get_jobs()


if __name__ == "__main__":
    asyncio.run(main())
