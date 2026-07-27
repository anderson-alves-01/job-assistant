from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    app_name: str = "Job Application Assistant API"
    app_version: str = "0.1.0"

    database_url: str = (
        "postgresql+psycopg://"
        "jobassistant:jobassistant@127.0.0.1:5433/jobassistant"
    )

    profile_path: Path = PROJECT_ROOT / "profile" / "profile.json"
    answers_path: Path = PROJECT_ROOT / "profile" / "answers.json"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / "backend" / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()