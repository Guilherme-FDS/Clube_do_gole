from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Pagamento


async def criar(db: AsyncSession, dados: dict) -> Pagamento:
    pagamento = Pagamento(**dados)
    db.add(pagamento)
    await db.flush()
    return pagamento


async def buscar_por_venda(db: AsyncSession, id_venda: int) -> list[Pagamento]:
    result = await db.execute(
        select(Pagamento).where(Pagamento.id_venda == id_venda)
    )
    return result.scalars().all()


async def listar_todos(db: AsyncSession) -> list[Pagamento]:
    result = await db.execute(
        select(Pagamento).order_by(Pagamento.criado_em.desc())
    )
    return result.scalars().all()


async def atualizar_gateway(db: AsyncSession, id_pagamento: int, dados: dict) -> None:
    """Atualiza campos vindos do gateway (status, metodo, gateway_id, pago_em...)."""
    from sqlalchemy import update
    await db.execute(
        update(Pagamento).where(Pagamento.id == id_pagamento).values(**dados)
    )


async def atualizar_status(db: AsyncSession, id_pagamento: int, status: str, pago_em=None) -> None:
    from datetime import datetime, timezone
    from sqlalchemy import update
    values = {"status": status}
    if pago_em:
        values["pago_em"] = pago_em
    await db.execute(
        update(Pagamento).where(Pagamento.id == id_pagamento).values(**values)
    )