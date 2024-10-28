from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASS: str
    PG_BASE: str

    REDIS_HOST: str
    REDIS_PORT: str

    model_config = SettingsConfigDict(env_file='../.env')


settings = Settings()
