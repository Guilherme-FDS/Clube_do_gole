# utils/auth.py
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from database.engine import get_db

settings = get_settings()
_bearer = HTTPBearer(auto_error=False)


def gerar_token(payload: dict[str, Any]) -> str:
    data = payload.copy()
    data["exp"] = datetime.now(timezone.utc) + timedelta(days=settings.jwt_expiry_days)
    return jwt.encode(data, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def _decode_token(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError:
        return None


async def _extrair_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente.")

    payload = _decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado.")

    # Admin não usa tabela de sessões — valida só o JWT
    if payload.get("tipo") == "admin":
        return payload

    # Cliente — valida sessão no banco
    jti = payload.get("jti")
    if not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token sem identificador de sessão.")

    from repositories.auth_repo import sessao_valida
    if not await sessao_valida(db, jti):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão encerrada ou expirada.")

    return payload


async def login_required(
    payload: dict[str, Any] = Depends(_extrair_payload),
) -> dict[str, Any]:
    return payload


async def admin_required(
    payload: dict[str, Any] = Depends(_extrair_payload),
) -> dict[str, Any]:
    if payload.get("tipo") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado.")
    return payload