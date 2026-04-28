import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:13421565@localhost:5432/clube_do_gole")


def get_connection():
    """Retorna uma conexão com o banco PostgreSQL."""
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def execute(query, params=None):
    """Executa INSERT/UPDATE/DELETE. Retorna linhas afetadas."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()
            return cur.rowcount


def fetchall(query, params=None):
    """Executa SELECT e retorna lista de dicts."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()


def fetchone(query, params=None):
    """Executa SELECT e retorna um dict ou None."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()


def test_connection():
    """Testa a conexão com o banco."""
    try:
        result = fetchone("SELECT version();")
        print(f"✅ Banco conectado: {result['version'][:50]}")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False


if __name__ == "__main__":
    test_connection()