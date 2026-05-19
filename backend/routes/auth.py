import secrets
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from database.engine import get_db
from database.models import UsuarioCliente
from repositories import carrinho_repo, auth_repo
from schemas import (
    LoginIn, CadastroIn, TokenOut, UsuarioOut,
    EsqueceuSenhaIn, RedefinirSenhaIn,
)
from utils.auth import gerar_token, login_required
from utils.email import send_reset_password_email
from config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=TokenOut)
async def login(body: LoginIn, db: AsyncSession = Depends(get_db)):
    adm = await auth_repo.autenticar_admin(db, body.email, body.senha)
    if adm:
        token = gerar_token({"id": adm.id, "email": adm.email, "tipo": "admin", "nome": adm.nome})
        return TokenOut(token=token, tipo="admin", nome=adm.nome)

    cliente = await auth_repo.autenticar_cliente(db, body.email, body.senha)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="E-mail ou senha inválidos.")

    itens_migrados = 0
    if body.guest_carrinho:
        itens_migrados = await carrinho_repo.inserir_guest(db, body.guest_carrinho, cliente.id)

    token = gerar_token({"id": cliente.id, "email": cliente.email, "tipo": "cliente", "nome": cliente.nome})
    return TokenOut(token=token, tipo="cliente", nome=cliente.nome, itens_migrados=itens_migrados)


@router.post("/cadastro", status_code=status.HTTP_201_CREATED)
async def cadastro(body: CadastroIn, db: AsyncSession = Depends(get_db)):
    if await auth_repo.email_existe(db, body.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado.")
    if await auth_repo.cpf_existe(db, body.cpf):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CPF já cadastrado.")
    await auth_repo.criar_cliente(db, body.model_dump())
    return {"message": "Cadastro realizado com sucesso."}


@router.get("/me", response_model=UsuarioOut)
async def me(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    cliente = await auth_repo.buscar_cliente(db, payload["id"])
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return cliente


@router.post("/logout")
async def logout(payload: dict = Depends(login_required), db: AsyncSession = Depends(get_db)):
    if payload.get("tipo") == "cliente":
        await carrinho_repo.limpar_ativos(db, payload["id"])
    return {"message": "Logout realizado."}


@router.post("/esqueceu-senha")
async def esqueceu_senha(body: EsqueceuSenhaIn, db: AsyncSession = Depends(get_db)):
    cliente = await auth_repo.buscar_cliente_por_email(db, body.email)
    if cliente:
        token = secrets.token_urlsafe(48)
        await auth_repo.salvar_token_reset(db, cliente.id, token, settings.reset_token_expire_minutes)
        await send_reset_password_email(cliente.email, cliente.nome, token)
    # Sempre retorna 200 — não revela se email existe
    return {"message": "Se este email estiver cadastrado, você receberá as instruções em breve."}


@router.post("/redefinir-senha")
async def redefinir_senha(body: RedefinirSenhaIn, db: AsyncSession = Depends(get_db)):
    from repositories.auth_repo import _hash
    token_obj = await auth_repo.buscar_token_reset(db, body.token)
    if not token_obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou já utilizado.")
    if token_obj.expira_em.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token expirado. Solicite um novo link.")
    cliente = await db.get(UsuarioCliente, token_obj.usuario_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    cliente.senha = _hash(body.nova_senha)
    await auth_repo.consumir_token_reset(db, token_obj)
    return {"message": "Senha redefinida com sucesso!"}