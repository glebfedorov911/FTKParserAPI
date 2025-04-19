from pydantic import BaseModel
from pydantic_settings import BaseSettings

import os


class DatabaseSettings(BaseModel):
    db_url: str = os.getenv("POSTGRES_URL")
    echo: bool = (os.getenv("DATABASE_ECHO") == "True")

class URL(BaseModel):
    prefix_ftk: str = "/ftk"
    tag_ftk: str = "FTK"

class Settings(BaseSettings):
    database_settings: DatabaseSettings = DatabaseSettings()
    url: URL = URL()

settings = Settings()