from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.vacancies.models import VacancyModel


class VacancyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_vacancies(self, limit: int, offset: int, q: str) -> Sequence[VacancyModel]:
        stmt = select(VacancyModel)

        if q:
            stmt = stmt.filter(
                VacancyModel.title.ilike(f"%{q}%")
                | VacancyModel.company.ilike(f"%{q}%")
                | VacancyModel.location.ilike(f"%{q}%")
            )

        stmt = stmt.limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_vacancy_by_id(self, vacancy_id: int) -> VacancyModel | None:
        return await self.db.get(VacancyModel, vacancy_id)
