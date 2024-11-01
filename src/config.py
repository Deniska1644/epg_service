from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PG_HOST: str
    PG_PORT: str
    PG_USER: str
    PG_PASS: str
    PG_BASE: str

    REDIS_HOST: str
    REDIS_PORT: str

    # auth settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITM: str

    model_config = SettingsConfigDict(env_file='../.env')

    def pg_url(self):
        return f"postgresql+asyncpg://{self.PG_USER}:{self.PG_PASS}@{self.PG_HOST}:{self.PG_PORT}/{self.PG_BASE}"


settings = Settings()
