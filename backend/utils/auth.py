from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from config import get_settings

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


def _extrair_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> dict[str, Any]:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ausente")
    payload = _decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")
    return payload


def login_required(
    payload: dict[str, Any] = Depends(_extrair_payload),
) -> dict[str, Any]:
    return payload


def admin_required(
    payload: dict[str, Any] = Depends(_extrair_payload),
) -> dict[str, Any]:
    if payload.get("tipo") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso negado")
    return payload