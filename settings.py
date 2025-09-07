from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Application settings
    ENV: str = "local"
    DEBUG: int = 0

    # Database settings
    DB_URL: str = "postgresql://postgres:password@localhost:5432/postgres"
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Gunicorn settings
    GUNICORN_WORKERS: int = 1
    GUNICORN_THREADS: int = 8
    GUNICORN_ACCESS_LOG: str = "-"
    GUNICORN_ERROR_LOG: str = "-"

    @field_validator("DEBUG", mode="before")
    @classmethod
    def validate_debug(cls, v: str) -> int:
        if int(v) in [0, 1]:
            return int(v)
        raise ValueError("DEBUG must be 0 or 1")

    @field_validator("GUNICORN_WORKERS", mode="before")
    @classmethod
    def validate_gunicorn_workers(cls, v: str) -> int:
        if int(v) > 0:
            return int(v)
        raise ValueError("GUNICORN_WORKERS must be a positive integer")

    @field_validator("GUNICORN_THREADS", mode="before")
    @classmethod
    def validate_gunicorn_threads(cls, v: str) -> int:
        if int(v) > 0:
            return int(v)
        raise ValueError("GUNICORN_THREADS must be a positive integer")


settings = Settings()
