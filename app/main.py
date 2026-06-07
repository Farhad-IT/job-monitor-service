from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.api.exception import AppException
from app.vacancies.router import router as vacancy_router
from app.api.lifespan import lifespan


app = FastAPI(lifespan=lifespan)
app.include_router(router=vacancy_router)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


