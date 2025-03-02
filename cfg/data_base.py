from os import getenv
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent

class DataBaseSettings(BaseSettings):
    # db_url: str = getenv("DATABASE_URL")
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/data.db"
    db_echo: bool = True

settings = DataBaseSettings()

settings.db_url
