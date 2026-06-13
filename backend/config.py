# config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Segurança ──────────────────────────────────────────────────────────────
    secret_key: str = "dev-secret-inseguro"
    jwt_secret: str = "dev-jwt-inseguro"
    jwt_algorithm: str = "HS256"
    jwt_expiry_days: int = 7

    # ── Banco de dados ─────────────────────────────────────────────────────────
    database_url: str = "sqlite+aiosqlite:///./database/clube_do_gole.db"

    # ── Servidor ───────────────────────────────────────────────────────────────
    port: int = 8000
    host: str = "0.0.0.0"
    env: str = "development"

    # ── CORS ───────────────────────────────────────────────────────────────────
    cors_origins: str = "http://localhost:5173"

    # ── Email ──────────────────────────────────────────────────────────────────
    gmail_user: str = ""
    gmail_app_password: str = ""
    frontend_url: str = "http://localhost:5173"
    reset_token_expire_minutes: int = 10

    # ── Admin inicial ──────────────────────────────────────────────────────────
    admin_email_inicial: str = "admin@clubedogole.com"
    # OBRIGATÓRIO em produção — sem default fraco
    admin_senha_inicial: str = "troque-esta-senha-admin"

    @property
    def admin_senha_segura(self) -> bool:
        return self.admin_senha_inicial != "troque-esta-senha-admin" and len(self.admin_senha_inicial) >= 12

    # ── Planos ─────────────────────────────────────────────────────────────────
    descontos_plano: dict = {"mensal": 0.00, "semestral": 0.05, "anual": 0.10}
    multiplicadores_plano: dict = {"mensal": 1, "semestral": 6, "anual": 12}

    # ── OAuth Google ───────────────────────────────────────────────────────────
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = "http://localhost:5173/auth/google/callback"

    # ── Mercado Pago ───────────────────────────────────────────────────────────
    mp_access_token: str = ""
    mp_public_key: str = ""
    # URL pública do backend (ngrok em dev, domínio em prod) — usada no webhook
    backend_public_url: str = "http://localhost:8000"

    # ── OAuth Facebook ─────────────────────────────────────────────────────────
    facebook_app_id: str = ""
    facebook_app_secret: str = ""
    facebook_redirect_uri: str = "http://localhost:5173/auth/facebook/callback"

    # ── Properties ─────────────────────────────────────────────────────────────
    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def mp_configured(self) -> bool:
        return bool(self.mp_access_token)

    @property
    def google_configured(self) -> bool:
        return bool(self.google_client_id and self.google_client_secret)

    @property
    def facebook_configured(self) -> bool:
        return bool(self.facebook_app_id and self.facebook_app_secret)


@lru_cache
def get_settings() -> Settings:
    return Settings()