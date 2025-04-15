from pydantic import BaseModel
from pydantic_settings import BaseSettings

import os


class DatabaseSettings(BaseModel):
    db_url: str = os.getenv("POSTGRES_URL")
    echo: bool = (os.getenv("DATABASE_ECHO") == "True")

class Settings(BaseSettings):
    database_settings: DatabaseSettings = DatabaseSettings()

settings = Settings()