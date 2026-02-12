import secrets

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ALGORITHM = "HS256"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 7 days = 7 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # database settings
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    def SQLALCHEMY_DATABASE_URI(self, sync: bool = False, test: bool = False) -> str:
        async_scheme = "postgresql+asyncpg"
        sync_scheme = "postgresql+psycopg2"

        return str(
            PostgresDsn.build(
                scheme=sync_scheme if sync else async_scheme,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=self.POSTGRES_PORT,
                path=(self.POSTGRES_DB if not test else f"{self.POSTGRES_DB}_test"),
            )
        )


settings = Settings()
