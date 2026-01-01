from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    DEBUG: bool = False

    # Citus Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str = "messages_db"
    POSTGRES_HOST: str = "citus-coordinator"
    POSTGRES_PORT: int = 5432

    POSTGRES_POOL_SIZE: int = 20
    POSTGRES_MAX_OVERFLOW: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Tarantool
    TARANTOOL_HOST: str = "tarantool"
    TARANTOOL_PORT: int = 3301
    TARANTOOL_USER: str = "admin"
    TARANTOOL_PASSWORD: str = "admin"

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    WEB_PORT: int = 8001


settings = AppSettings()
