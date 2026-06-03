from datetime import date, datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Assinatura


async def criar(db: AsyncSession, dados: dict) -> Assinatura:
    assinatura = Assinatura(**dados)
    db.add(assinatura)
    await db.flush()
    return assinatura


async def buscar_por_cliente(db: AsyncSession, id_cliente: int) -> list[Assinatura]:
    result = await db.execute(
        select(Assinatura)
        .where(Assinatura.id_cliente == id_cliente)
        .order_by(Assinatura.criado_em.desc())
    )
    return result.scalars().all()


async def buscar_ativa_por_cliente(db: AsyncSession, id_cliente: int) -> Assinatura | None:
    result = await db.execute(
        select(Assinatura)
        .where(Assinatura.id_cliente == id_cliente, Assinatura.status == "ativa")
    )
    return result.scalar_one_or_none()


async def listar_todas(db: AsyncSession) -> list[Assinatura]:
    result = await db.execute(
        select(Assinatura).order_by(Assinatura.criado_em.desc())
    )
    return result.scalars().all()


async def atualizar_status(db: AsyncSession, id_assinatura: int, status: str) -> None:
    await db.execute(
        update(Assinatura)
        .where(Assinatura.id == id_assinatura)
        .values(status=status, atualizado_em=datetime.now(timezone.utc))
    )