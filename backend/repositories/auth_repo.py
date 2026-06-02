# repositories/auth_repo.py
import bcrypt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import UsuarioAdm, UsuarioCliente, PasswordResetToken, SessaoUsuario


# ── Helpers ────────────────────────────────────────────────────────────────────

def _check(senha_raw: str, senha_hash: str) -> bool:
    try:
        return bcrypt.checkpw(senha_raw.encode(), senha_hash.encode())
    except Exception:
        return False

def _hash(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


# ── Admin ──────────────────────────────────────────────────────────────────────

async def autenticar_admin(db: AsyncSession, email: str, senha: str) -> UsuarioAdm | None:
    adm = await db.scalar(select(UsuarioAdm).where(UsuarioAdm.email == email.lower()))
    return adm if adm and _check(senha, adm.senha) else None


# ── Cliente local ──────────────────────────────────────────────────────────────

async def autenticar_cliente(db: AsyncSession, email: str, senha: str) -> UsuarioCliente | None:
    c = await db.scalar(
        select(UsuarioCliente).where(
            UsuarioCliente.email == email.lower(),
            UsuarioCliente.ativo == True,
        )
    )
    if not c or not c.senha:
        return None
    return c if _check(senha, c.senha) else None


async def email_existe(db: AsyncSession, email: str) -> bool:
    return await db.scalar(
        select(UsuarioCliente.id).where(UsuarioCliente.email == email.lower())
    ) is not None


async def cpf_existe(db: AsyncSession, cpf: str) -> bool:
    return await db.scalar(
        select(UsuarioCliente.id).where(UsuarioCliente.cpf == cpf)
    ) is not None


async def criar_cliente(db: AsyncSession, dados: dict) -> UsuarioCliente:
    c = UsuarioCliente(
        cpf=dados["cpf"],
        nome=dados["nome"],
        sobrenome=dados["sobrenome"],
        data_nascimento=dados.get("data_nascimento"),
        email=dados["email"].lower(),
        senha=_hash(dados["senha"]),
        telefone=dados.get("telefone"),
    )
    db.add(c)
    await db.flush()
    await db.refresh(c)
    return c


async def buscar_cliente(db: AsyncSession, usuario_id: int) -> UsuarioCliente | None:
    return await db.get(UsuarioCliente, usuario_id)


async def buscar_cliente_por_email(db: AsyncSession, email: str) -> UsuarioCliente | None:
    return await db.scalar(
        select(UsuarioCliente).where(UsuarioCliente.email == email.lower())
    )


async def listar_clientes(db: AsyncSession) -> list[UsuarioCliente]:
    return list((await db.scalars(
        select(UsuarioCliente).order_by(UsuarioCliente.id)
    )).all())


async def atualizar_cliente(db: AsyncSession, usuario_id: int, dados: dict) -> UsuarioCliente:
    c = await db.get(UsuarioCliente, usuario_id)
    c.nome = dados["nome"]
    c.sobrenome = dados["sobrenome"]
    c.email = dados["email"].lower()
    c.telefone = dados.get("telefone")
    c.data_nascimento = dados.get("data_nascimento")
    await db.flush()
    await db.refresh(c)
    return c


async def alterar_senha(db: AsyncSession, usuario_id: int, senha_atual: str, nova_senha: str) -> tuple[bool, str]:
    c = await db.get(UsuarioCliente, usuario_id)
    if not c:
        return False, "Usuário não encontrado."
    if not c.senha:
        return False, "Esta conta usa login social. Defina uma senha nas configurações."
    if not _check(senha_atual, c.senha):
        return False, "Senha atual incorreta."
    c.senha = _hash(nova_senha)
    await db.flush()
    return True, "Senha alterada com sucesso!"


# ── OAuth ──────────────────────────────────────────────────────────────────────

async def buscar_ou_criar_oauth(
    db: AsyncSession,
    email: str,
    nome: str,
    sobrenome: str,
    provider: str,
    provider_id: str,
) -> UsuarioCliente:
    # 1. Busca por provider_id (login repetido com o mesmo social)
    c = await db.scalar(
        select(UsuarioCliente).where(
            UsuarioCliente.provider == provider,
            UsuarioCliente.provider_id == provider_id,
        )
    )
    if c:
        return c

    # 2. Busca por email (conta local já existe — vincula)
    c = await db.scalar(
        select(UsuarioCliente).where(UsuarioCliente.email == email.lower())
    )
    if c:
        c.provider = provider
        c.provider_id = provider_id
        await db.flush()
        await db.refresh(c)
        return c

    # 3. Cria conta nova via OAuth
    c = UsuarioCliente(
        email=email.lower(),
        nome=nome,
        sobrenome=sobrenome,
        provider=provider,
        provider_id=provider_id,
    )
    db.add(c)
    await db.flush()
    await db.refresh(c)
    return c


# ── Sessões ────────────────────────────────────────────────────────────────────

async def criar_sessao(
    db: AsyncSession,
    usuario_id: int,
    jti: str,
    expira_em: datetime,
    dispositivo: str | None = None,
    ip: str | None = None,
) -> SessaoUsuario:
    s = SessaoUsuario(
        id_usuario=usuario_id,
        token_jti=jti,
        expira_em=expira_em,
        dispositivo=dispositivo,
        ip=ip,
    )
    db.add(s)
    await db.flush()
    return s


async def revogar_sessao(db: AsyncSession, jti: str) -> None:
    s = await db.scalar(select(SessaoUsuario).where(SessaoUsuario.token_jti == jti))
    if s:
        s.revogado = True
        await db.flush()


async def sessao_valida(db: AsyncSession, jti: str) -> bool:
    s = await db.scalar(select(SessaoUsuario).where(SessaoUsuario.token_jti == jti))
    if not s or s.revogado:
        return False
    return s.expira_em.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)


# ── Reset de senha ─────────────────────────────────────────────────────────────

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