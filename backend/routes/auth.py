# routes/auth.py
import secrets
import uuid
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_settings
from database.engine import get_db
from database.models import UsuarioCliente
from repositories import auth_repo, carrinho_repo
from schemas import (
    CadastroIn, EsqueceuSenhaIn, LoginIn,
    OAuthCallbackIn, RedefinirSenhaIn, TokenOut, UsuarioOut,
)
from utils.auth import gerar_token, login_required
from utils.email import send_reset_password_email
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

settings = get_settings()
router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── Helpers internos ───────────────────────────────────────────────────────────

def _gerar_token_com_sessao(cliente: UsuarioCliente) -> str:
    jti = str(uuid.uuid4())
    expira_em = datetime.utcnow() + timedelta(days=settings.jwt_expiry_days)
    return gerar_token({
        "id": cliente.id,
        "email": cliente.email,
        "tipo": "cliente",
        "nome": cliente.nome,
        "jti": jti,
    }), jti, expira_em


# ── Login / Cadastro ───────────────────────────────────────────────────────────

@router.post("/login", response_model=TokenOut)
@limiter.limit("10/minute")
async def login(request: Request, body: LoginIn, db: AsyncSession = Depends(get_db)):
    adm = await auth_repo.autenticar_admin(db, body.email, body.senha)
    if adm:
        token = gerar_token({"id": adm.id, "email": adm.email, "tipo": "admin", "nome": adm.nome})
        return TokenOut(token=token, tipo="admin", nome=adm.nome)

    cliente = await auth_repo.autenticar_cliente(db, body.email, body.senha)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha inválidos.")

    token, jti, expira_em = _gerar_token_com_sessao(cliente)

    await auth_repo.criar_sessao(
        db, cliente.id, jti, expira_em,
        dispositivo=request.headers.get("user-agent"),
        ip=request.client.host if request.client else None,
    )

    itens_migrados = 0
    if body.guest_carrinho:
        itens_migrados = await carrinho_repo.inserir_guest(db, body.guest_carrinho, cliente.id)

    return TokenOut(token=token, tipo="cliente", nome=cliente.nome, itens_migrados=itens_migrados)


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
async def cadastro(body: CadastroIn, db: AsyncSession = Depends(get_db)):
    if await auth_repo.email_existe(db, body.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado.")
    if await auth_repo.cpf_existe(db, body.cpf):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF já cadastrado.")
    await auth_repo.criar_cliente(db, body.model_dump())
    return {"message": "Cadastro realizado com sucesso."}


# ── OAuth ──────────────────────────────────────────────────────────────────────

@router.post("/oauth/callback", response_model=TokenOut)
async def oauth_callback(body: OAuthCallbackIn, request: Request, db: AsyncSession = Depends(get_db)):
    if body.provider == "google":
        user_info = await _trocar_code_google(body.code)
    elif body.provider == "facebook":
        user_info = await _trocar_code_facebook(body.code)
    else:
        raise HTTPException(status_code=400, detail="Provider inválido.")

    cliente = await auth_repo.buscar_ou_criar_oauth(
        db,
        email=user_info["email"],
        nome=user_info["nome"],
        sobrenome=user_info["sobrenome"],
        provider=body.provider,
        provider_id=user_info["provider_id"],
    )

    if not cliente.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conta desativada.")

    token, jti, expira_em = _gerar_token_com_sessao(cliente)

    await auth_repo.criar_sessao(
        db, cliente.id, jti, expira_em,
        dispositivo=request.headers.get("user-agent"),
        ip=request.client.host if request.client else None,
    )

    itens_migrados = 0
    if body.guest_carrinho:
        itens_migrados = await carrinho_repo.inserir_guest(db, body.guest_carrinho, cliente.id)

    return TokenOut(token=token, tipo="cliente", nome=cliente.nome, itens_migrados=itens_migrados)


async def _trocar_code_google(code: str) -> dict:
    if not settings.google_configured:
        raise HTTPException(status_code=503, detail="Login com Google não configurado.")

    async with httpx.AsyncClient() as client:
        # Troca code pelo access_token
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Falha ao autenticar com Google.")

        access_token = token_res.json().get("access_token")

        # Busca dados do usuário
        user_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Falha ao obter dados do Google.")

        data = user_res.json()
        return {
            "email": data["email"],
            "nome": data.get("given_name", data.get("name", "Usuário")),
            "sobrenome": data.get("family_name", ""),
            "provider_id": data["id"],
        }


async def _trocar_code_facebook(code: str) -> dict:
    if not settings.facebook_configured:
        raise HTTPException(status_code=503, detail="Login com Facebook não configurado.")

    async with httpx.AsyncClient() as client:
        # Troca code pelo access_token
        token_res = await client.get(
            "https://graph.facebook.com/v19.0/oauth/access_token",
            params={
                "client_id": settings.facebook_app_id,
                "client_secret": settings.facebook_app_secret,
                "redirect_uri": settings.facebook_redirect_uri,
                "code": code,
            },
        )
        if token_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Falha ao autenticar com Facebook.")

        access_token = token_res.json().get("access_token")

        # Busca dados do usuário
        user_res = await client.get(
            "https://graph.facebook.com/me",
            params={
                "fields": "id,email,first_name,last_name",
                "access_token": access_token,
            },
        )
        if user_res.status_code != 200:
            raise HTTPException(status_code=400, detail="Falha ao obter dados do Facebook.")

        data = user_res.json()
        return {
            "email": data.get("email", ""),
            "nome": data.get("first_name", "Usuário"),
            "sobrenome": data.get("last_name", ""),
            "provider_id": data["id"],
        }


# ── Sessão / Perfil ────────────────────────────────────────────────────────────

@router.get("/me", response_model=UsuarioOut)
async def me(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    cliente = await auth_repo.buscar_cliente(db, payload["id"])
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return cliente


@router.post("/logout")
async def logout(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    jti = payload.get("jti")
    if jti:
        await auth_repo.revogar_sessao(db, jti)
    if payload.get("tipo") == "cliente":
        await carrinho_repo.limpar_ativos(db, payload["id"])
    return {"message": "Logout realizado."}


# ── Recuperação de senha ───────────────────────────────────────────────────────

@router.post("/esqueceu-senha")
@limiter.limit("5/minute")
async def esqueceu_senha(request: Request, body: EsqueceuSenhaIn, db: AsyncSession = Depends(get_db)):
    cliente = await auth_repo.buscar_cliente_por_email(db, body.email)
    if cliente:
        token = secrets.token_urlsafe(48)
        await auth_repo.salvar_token_reset(db, cliente.id, token, settings.reset_token_expire_minutes)
        await send_reset_password_email(cliente.email, cliente.nome, token)
    return {"message": "Se este email estiver cadastrado, você receberá as instruções em breve."}


@router.post("/redefinir-senha")
async def redefinir_senha(body: RedefinirSenhaIn, db: AsyncSession = Depends(get_db)):
    token_obj = await auth_repo.buscar_token_reset(db, body.token)
    if not token_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou já utilizado.")
    if token_obj.expira_em.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expirado. Solicite um novo link.")
    cliente = await db.get(UsuarioCliente, token_obj.usuario_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    cliente.senha = auth_repo._hash(body.nova_senha)
    await auth_repo.consumir_token_reset(db, token_obj)
    return {"message": "Senha redefinida com sucesso!"}