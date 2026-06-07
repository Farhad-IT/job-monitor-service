import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str

def get_settings() -> Settings:
    url = DATABASE_URL
    return Settings(
        DATABASE_URL=url,
    )

settings = get_settings()