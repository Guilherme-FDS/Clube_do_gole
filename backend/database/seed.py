import os
import bcrypt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import UsuarioAdm, DescontoPlan


async def seed(session: AsyncSession) -> None:
    await _seed_admin(session)
    await _seed_descontos(session)
    await session.commit()


async def _seed_admin(session: AsyncSession) -> None:
    existe = await session.scalar(select(UsuarioAdm).limit(1))
    if existe:
        return

    senha_raw = os.getenv("ADMIN_SENHA_INICIAL", "troque-esta-senha-admin")
    senha_hash = bcrypt.hashpw(senha_raw.encode(), bcrypt.gensalt()).decode()

    session.add(UsuarioAdm(
        nome="Administrador",
        email=os.getenv("ADMIN_EMAIL_INICIAL", "admin@clubedogole.com"),
        senha=senha_hash,
        tipo="admin",
    ))


async def _seed_descontos(session: AsyncSession) -> None:
    existe = await session.scalar(select(DescontoPlan).limit(1))
    if existe:
        return

    session.add_all([
        DescontoPlan(plano="mensal",    desconto=0.00),
        DescontoPlan(plano="semestral", desconto=5.00),
        DescontoPlan(plano="anual",     desconto=10.00),
    ])