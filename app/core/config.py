from os import environ

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Base Project"
    VERSION: str = "1.0.0"
    ADMIN_API_VERSION: str = "/v1"
    API_VERSION: str = "/v1"
    DOMAIN: str = "http://127.0.0.1:8000"
    ENVIRONMENT: str = "dev"
    DEBUG: bool = True

    POSTGRES_SERVER: str = environ.get("POSTGRESQL_HOST", "localhost")
    POSTGRES_USER: str = environ.get("POSTGRESQL_USER", "postgres")
    POSTGRES_PASSWORD: str = environ.get("POSTGRESQL_PASSWORD", "")
    POSTGRES_DB: str = environ.get("POSTGRESQL_DB", "base")

    SUPER_ADMIN_EMAIL: str = environ.get("SUPER_ADMIN_EMAIL", "admin@moigate.com")
    SUPER_ADMIN_PASSWORD: str = environ.get("SUPER_ADMIN_PASSWORD", "admin")
    SECRET_KEY: str = environ.get("SECRET_KEY", "secret")

    @property
    def get_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"


settings = Settings()
