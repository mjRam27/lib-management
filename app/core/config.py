"""Application settings, loaded from environment variables or a .env file."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration. Override any value with an env var prefixed `LIB_`."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="LIB_", extra="ignore")

    app_name: str = "Library Management System"
    app_version: str = "1.0.0"
    api_v1_prefix: str = "/api/v1"
    seed_sample_data: bool = True

    # Lending rules
    default_loan_days: int = 14
    max_loan_days: int = 60
    max_loans_standard: int = 3
    max_loans_premium: int = 10
    max_renewals: int = 2
    fine_per_day: float = 1.0


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()
