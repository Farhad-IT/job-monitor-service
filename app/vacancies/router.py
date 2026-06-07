from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_vacancies_service
from app.vacancies.schema import VacancySchema
from app.vacancies.service import VacancyService

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

VacancyServiceDep = Annotated[VacancyService, Depends(get_vacancies_service)]

@router.get("", status_code=200)
async def get_vacancies(
        vacancies_service: VacancyServiceDep,
        limit: int | None = 10,
        page: int | None = 1,
        q: str | None = Query(default=None),
) -> list[VacancySchema]:
    return await vacancies_service.get_vacancies(
        limit=limit,
        page=page,
        q=q,
    )


@router.get("/{vacancy_id}", status_code=200)
async def get_vacancy_by_id(
        vacancies_service: VacancyServiceDep,
        vacancy_id: int,
) -> VacancySchema | None:
    return await vacancies_service.get_vacancy_by_id(vacancy_id=vacancy_id)

