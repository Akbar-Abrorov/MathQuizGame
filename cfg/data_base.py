from os import getenv
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class DataBaseSettings(BaseSettings):
    # db_url: str = getenv("DATABASE_URL")
    api_v1_prefix: str = getenv("API_V1_PREFIX", "/api/v1")
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/data.db"
    db_echo: bool = True

settings = DataBaseSettings()

settings.db_url
