"""Project Settings"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@0.0.0.0:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


db_settings = DBSettings()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

SECRET_KEY = "somesecretekey"

ALGORITHM = "HS256"
