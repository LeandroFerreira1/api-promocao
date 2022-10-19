from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    #DB_URL: str = 'postgresql+asyncpg://postgres:1702@localhost:5432/promocao'
    #DB_URL: str = 'postgresql+asyncpg://admin:admin@localhost:5432/promo'
    DB_URL: str = 'postgresql+asyncpg://postgres:589916@191.253.23.111:3152/promocao'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = '81ZONkehu3qVaSKG0iAXrNAW97eMu62VobhRyEIeV3M'
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'
    # 60 minutos * 24 horas * 7 dias => 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
