import bcrypt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import UsuarioAdm, UsuarioCliente, PasswordResetToken


def _check(senha_raw: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha_raw.encode(), senha_hash.encode())
    except Exception:
        return False

def _hash(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


async def autenticar_admin(db: AsyncSession, email: str, senha: str) -> UsuarioAdm | None:
    adm = await db.scalar(select(UsuarioAdm).where(UsuarioAdm.email == email.lower()))
    return adm if adm and _check(senha, adm.senha) else None

async def autenticar_cliente(db: AsyncSession, email: str, senha: str) -> UsuarioCliente | None:
    c = await db.scalar(select(UsuarioCliente).where(UsuarioCliente.email == email.lower()))
    return c if c and _check(senha, c.senha) else None

async def email_existe(db: AsyncSession, email: str) -> bool:
    return await db.scalar(select(UsuarioCliente.id).where(UsuarioCliente.email == email.lower())) is not None

async def cpf_existe(db: AsyncSession, cpf: str) -> bool:
    return await db.scalar(select(UsuarioCliente.id).where(UsuarioCliente.cpf == cpf)) is not None

async def criar_cliente(db: AsyncSession, dados: dict) -> UsuarioCliente:
    c = UsuarioCliente(
        cpf=dados["cpf"], nome=dados["nome"], sobrenome=dados["sobrenome"],
        data_nascimento=dados.get("data_nascimento"),
        email=dados["email"].lower(), senha=_hash(dados["senha"]),
        telefone=dados.get("telefone"),
    )
    db.add(c); await db.flush(); await db.refresh(c)
    return c

async def buscar_cliente(db: AsyncSession, usuario_id: int) -> UsuarioCliente | None:
    return await db.get(UsuarioCliente, usuario_id)

async def buscar_cliente_por_email(db: AsyncSession, email: str) -> UsuarioCliente | None:
    return await db.scalar(select(UsuarioCliente).where(UsuarioCliente.email == email.lower()))

async def listar_clientes(db: AsyncSession) -> list[UsuarioCliente]:
    return list((await db.scalars(select(UsuarioCliente).order_by(UsuarioCliente.id))).all())

async def atualizar_cliente(db: AsyncSession, usuario_id: int, dados: dict) -> UsuarioCliente:
    c = await db.get(UsuarioCliente, usuario_id)
    c.nome = dados["nome"]; c.sobrenome = dados["sobrenome"]
    c.email = dados["email"].lower(); c.telefone = dados.get("telefone")
    c.data_nascimento = dados.get("data_nascimento")
    await db.flush(); await db.refresh(c)
    return c

async def alterar_senha(db: AsyncSession, usuario_id: int, senha_atual: str, nova_senha: str) -> tuple[bool, str]:
    c = await db.get(UsuarioCliente, usuario_id)
    if not c: return False, "Usuário não encontrado."
    if not _check(senha_atual, c.senha): return False, "Senha atual incorreta."
    c.senha = _hash(nova_senha); await db.flush()
    return True, "Senha alterada com sucesso!"

async def salvar_token_reset(db: AsyncSession, usuario_id: int, token: str, expire_minutes: int) -> None:
    await db.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.usuario_id == usuario_id)
        .values(usado=True)
    )
    db.add(PasswordResetToken(
        usuario_id=usuario_id,
        token=token,
        expira_em=datetime.now(timezone.utc) + timedelta(minutes=expire_minutes),
    ))
    await db.flush()

async def buscar_token_reset(db: AsyncSession, token: str) -> PasswordResetToken | None:
    return await db.scalar(
        select(PasswordResetToken).where(
            PasswordResetToken.token == token,
            PasswordResetToken.usado == False,
        )
    )

async def consumir_token_reset(db: AsyncSession, token_obj: PasswordResetToken) -> None:
    token_obj.usado = True
    await db.flush()