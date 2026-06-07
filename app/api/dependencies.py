from app.subscription.repository import SubscribeRepository
from app.user.repository import UserRepository
from app.vacancies.service import VacancyService
from app.db.session import SessionDep


def get_vacancies_service(db: SessionDep):
    return VacancyService(db)


def get_users_repository(db: SessionDep):
    return UserRepository(db)

def get_subscribe_repository(db: SessionDep):
    return SubscribeRepository(db)