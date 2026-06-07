from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exception import NotFoundException
from app.vacancies.repository import VacancyRepository
from app.vacancies.schema import VacancySchema


class VacancyService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.vacancy_repository = VacancyRepository(db)

    async def get_vacancies(self, limit: int, page: int, q: str) -> list[VacancySchema]:
        page = max(page, 1)
        limit = min(limit, 50)
        offset = (page - 1) * limit
        jobs = await self.vacancy_repository.get_vacancies(limit=limit, offset=offset, q=q)
        print(len(jobs))
        return [VacancySchema.model_validate(job) for job in jobs]

    async def get_vacancy_by_id(self, vacancy_id: int) -> VacancySchema | None:
        vacancy = await self.vacancy_repository.get_vacancy_by_id(vacancy_id=vacancy_id)

        if not vacancy:
            raise NotFoundException("Vacancy not found")

        return VacancySchema.model_validate(vacancy)
