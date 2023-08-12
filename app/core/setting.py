import os.path
from functools import lru_cache
from os import path, environ

from pydantic_settings import BaseSettings, SettingsConfigDict


def get_env_filepath() -> str:
    base_path = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    file_path = os.path.join(base_path, environ.get("PROJECT_ENV", ".env.local"))
    if not os.path.exists(file_path):
        raise Exception(f"Not exists file: {file_path}")
    return file_path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_filepath())
    # env
    title: str = "Jira Action"
    description: str = "Jira Action For CI/CD"
    debug: bool
    reload: bool
    host: str
    port: int
    workers: int
    use_colors: bool
    api_key: str


@lru_cache()
def get_cached_settings() -> Settings:
    return Settings()
