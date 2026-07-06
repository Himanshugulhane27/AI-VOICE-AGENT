"""Application settings loaded from environment variables.

Uses pydantic-settings for typed, validated configuration with
automatic .env file loading via python-dotenv.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralised application configuration.

    Values are read from environment variables (case-insensitive) and
    fall back to the defaults declared here.  A ``.env`` file in the
    project root is loaded automatically when present.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # ---- Server -----------------------------------------------------------
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"

    # ---- Google Sheets -----------------------------------------------------
    google_sheet_id: str = ""
    google_service_account_file: str = ""

    # ---- Email / SMTP ------------------------------------------------------
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = ""

    # ---- RetellAI (future) ------------------------------------------------
    retell_api_key: str = ""


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached singleton of the application settings.

    The ``lru_cache`` decorator ensures the ``.env`` file is read only
    once and the same ``Settings`` instance is reused for the lifetime
    of the process.
    """
    return Settings()
