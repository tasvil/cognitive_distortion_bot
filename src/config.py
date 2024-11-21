from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from data.white_list import (
    ALLOWED_IDS as default_allowed_ids,
    TESTER_IDS as default_tester_ids,
)


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: SecretStr
    OPENAI_API_KEY: SecretStr
    DATABASE_URL: str

    ALLOWED_IDS: list[int] = default_allowed_ids
    TESTER_IDS: list[int] = default_tester_ids

    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")


config = Settings()
print(config.DATABASE_URL)