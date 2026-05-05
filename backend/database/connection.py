import os
import sqlite3
import re
from dotenv import load_dotenv

load_dotenv()

# ==============================================================
# MODO DE BANCO DE DADOS
# --------------------------------------------------------------
# Durante o desenvolvimento, usamos SQLite para rodar em qualquer
# máquina sem precisar instalar o PostgreSQL.
#
# Para produção, basta:
#   1. Comentar o bloco SQLITE abaixo
#   2. Descomentar o bloco POSTGRESQL
#   3. Garantir que DATABASE_URL está no .env
# ==============================================================


# --------------------------------------------------------------
# [ATIVO] SQLite — desenvolvimento local
# --------------------------------------------------------------
DB_MODE = "sqlite"
SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "clube_do_gole.db")


# --------------------------------------------------------------
# [PRODUÇÃO] PostgreSQL — descomentar quando subir em produção
# --------------------------------------------------------------
# import psycopg
# from psycopg.rows import dict_row
#
# DB_MODE = "postgresql"
# DATABASE_URL = os.getenv(
#     "DATABASE_URL",
#     "postgresql://postgres:postgres@localhost:5432/clube_do_gole"
# )
# --------------------------------------------------------------


def _pg_to_sqlite(query: str) -> str:
    """
    Converte sintaxe PostgreSQL -> SQLite:
      - %s  ->  ?
      - SERIAL  ->  INTEGER
      - gen_random_uuid()  ->  UUID via hex(randomblob)
      - NOW()  ->  CURRENT_TIMESTAMP
      - BOOLEAN  ->  INTEGER
      - ::text / ::int (casts)  ->  removidos
    """
    query = query.replace("%s", "?")
    query = re.sub(r"\bSERIAL\b", "INTEGER", query, flags=re.IGNORECASE)
    query = re.sub(r"\bNOW\(\)", "CURRENT_TIMESTAMP", query, flags=re.IGNORECASE)
    query = re.sub(r"\bBOOLEAN\b", "INTEGER", query, flags=re.IGNORECASE)
    query = re.sub(r"::\w+", "", query)

    uuid_expr = (
        "(lower(hex(randomblob(4)))||'-'||lower(hex(randomblob(2)))||'-4'||"
        "substr(lower(hex(randomblob(2))),2)||'-'||"
        "substr('89ab',abs(random())%4+1,1)||"
        "substr(lower(hex(randomblob(2))),2)||'-'||lower(hex(randomblob(6))))"
    )
    query = re.sub(r"\bgen_random_uuid\(\)", uuid_expr, query, flags=re.IGNORECASE)

    return query


def _row_to_dict(cursor: sqlite3.Cursor, row) -> dict:
    """Converte uma linha do SQLite em dict usando os nomes das colunas."""
    cols = [d[0] for d in cursor.description]
    return dict(zip(cols, row))


def _get_sqlite_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


# ==============================================================
# API PÚBLICA — mesma interface para SQLite e PostgreSQL
# ==============================================================

def get_connection():
    """Retorna uma conexão com o banco ativo."""
    if DB_MODE == "sqlite":
        return _get_sqlite_connection()
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)  # noqa: F821


def execute(query: str, params=None):
    """Executa INSERT / UPDATE / DELETE. Retorna linhas afetadas."""
    if DB_MODE == "sqlite":
        query = _pg_to_sqlite(query)
        with _get_sqlite_connection() as conn:
            cur = conn.execute(query, params or ())
            conn.commit()
            return cur.rowcount

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            conn.commit()
            return cur.rowcount


def fetchall(query: str, params=None) -> list:
    """Executa SELECT e retorna lista de dicts."""
    if DB_MODE == "sqlite":
        query = _pg_to_sqlite(query)
        with _get_sqlite_connection() as conn:
            cur = conn.execute(query, params or ())
            rows = cur.fetchall()
            return [_row_to_dict(cur, r) for r in rows]

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchall()


def fetchone(query: str, params=None):
    """Executa SELECT e retorna um dict ou None."""
    if DB_MODE == "sqlite":
        query = _pg_to_sqlite(query)
        with _get_sqlite_connection() as conn:
            cur = conn.execute(query, params or ())
            row = cur.fetchone()
            return _row_to_dict(cur, row) if row else None

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params or ())
            return cur.fetchone()


# ==============================================================
# INICIALIZAÇÃO DO BANCO SQLITE
# ==============================================================

def init_sqlite():
    """Cria o schema SQLite a partir do init.sql na primeira execução."""
    if DB_MODE != "sqlite":
        return

    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init.sql")
    if not os.path.exists(schema_path):
        print("init.sql não encontrado.")
        return

    with open(schema_path, "r", encoding="utf-8") as f:
        raw_sql = f.read()

    raw_sql = re.sub(
        r"CREATE EXTENSION.*?;", "", raw_sql, flags=re.IGNORECASE | re.DOTALL
    )
    sql = _pg_to_sqlite(raw_sql)

    with _get_sqlite_connection() as conn:
        try:
            conn.executescript(sql)
            print(f"✅ SQLite inicializado em: {SQLITE_PATH}")
        except Exception as e:
            print(f"⚠️  Aviso ao inicializar SQLite: {e}")


def test_connection():
    """Testa a conexão com o banco ativo."""
    try:
        if DB_MODE == "sqlite":
            result = fetchone("SELECT sqlite_version() AS version")
            print(f"✅ SQLite conectado — versão: {result['version']}")
        else:
            result = fetchone("SELECT version();")
            print(f"✅ PostgreSQL conectado: {result['version'][:50]}")
        return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False


# Inicializa automaticamente ao importar (só na primeira vez)
if DB_MODE == "sqlite":
    init_sqlite()


if __name__ == "__main__":
    test_connection()