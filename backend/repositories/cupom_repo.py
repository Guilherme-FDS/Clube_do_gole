from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import Cupom


async def listar(db: AsyncSession) -> list[Cupom]:
    return list((await db.scalars(select(Cupom).order_by(Cupom.id))).all())

async def buscar_por_id(db: AsyncSession, cupom_id: int) -> Cupom | None:
    return await db.get(Cupom, cupom_id)

async def buscar_por_codigo(db: AsyncSession, codigo: str) -> Cupom | None:
    return await db.scalar(select(Cupom).where(Cupom.codigo == codigo.upper()))

async def criar(db: AsyncSession, dados: dict) -> Cupom:
    c = Cupom(**dados); db.add(c)
    await db.flush(); await db.refresh(c)
    return c

async def atualizar(db: AsyncSession, cupom_id: int, dados: dict) -> Cupom | None:
    c = await db.get(Cupom, cupom_id)
    if not c: return None
    for k, v in dados.items(): setattr(c, k, v)
    await db.flush(); await db.refresh(c)
    return c

async def remover(db: AsyncSession, cupom_id: int) -> bool:
    c = await db.get(Cupom, cupom_id)
    if not c: return False
    await db.delete(c); await db.flush()
    return True

async def consumir_atomico(db: AsyncSession, codigo: str) -> bool:
    """WHERE usos_restantes > 0 garante atomicidade — resolve race condition."""
    result = await db.execute(
        update(Cupom)
        .where(Cupom.codigo == codigo.upper(), Cupom.usos_restantes > 0)
        .values(usos_restantes=Cupom.usos_restantes - 1)
    )
    return result.rowcount > 0