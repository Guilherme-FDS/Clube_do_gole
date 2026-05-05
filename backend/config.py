import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    JWT_SECRET = os.getenv("JWT_SECRET", SECRET_KEY)
    PORT       = int(os.getenv("PORT", 5000))

    # ----------------------------------------------------------
    # [ATIVO] SQLite — desenvolvimento local
    # ----------------------------------------------------------
    DATABASE_URL = "sqlite:///database/clube_do_gole.db"

    # ----------------------------------------------------------
    # [PRODUÇÃO] PostgreSQL — descomentar junto com connection.py
    # ----------------------------------------------------------
    # DATABASE_URL = os.getenv(
    #     "DATABASE_URL",
    #     "postgresql://postgres:postgres@localhost:5432/clube_do_gole"
    # )

    DESCONTOS_PLANO       = {"mensal": 0.00, "semestral": 0.05, "anual": 0.10}
    MULTIPLICADORES_PLANO = {"mensal": 1,    "semestral": 6,    "anual": 12}