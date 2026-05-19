from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    secret_key: str = "dev-secret-inseguro"
    jwt_secret: str = "dev-jwt-inseguro"
    jwt_algorithm: str = "HS256"
    jwt_expiry_days: int = 7

    database_url: str = "sqlite+aiosqlite:///./database/clube_do_gole.db"

    port: int = 8000
    host: str = "0.0.0.0"
    env: str = "development"

    cors_origins: str = "http://localhost:5173"

    gmail_user: str = ""
    gmail_app_password: str = ""
    frontend_url: str = "http://localhost:5173"
    reset_token_expire_minutes: int = 10

    admin_email_inicial: str = "admin@clubedogole.com"
    admin_senha_inicial: str = "troque-esta-senha-admin"

    descontos_plano: dict = {"mensal": 0.00, "semestral": 0.05, "anual": 0.10}
    multiplicadores_plano: dict = {"mensal": 1, "semestral": 6, "anual": 12}

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")


@lru_cache
def get_settings() -> Settings:
    return Settings()