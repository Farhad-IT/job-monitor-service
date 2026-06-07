from pydantic import BaseModel, ConfigDict


class VacancySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str
    company: str
    title: str
    location: str
    url: str