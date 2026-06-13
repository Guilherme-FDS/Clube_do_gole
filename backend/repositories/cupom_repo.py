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
    """Decrementa usos_restantes só quando há limite de quantidade definido."""
    from sqlalchemy import or_
    result = await db.execute(
        update(Cupom)
        .where(
            Cupom.codigo == codigo.upper(),
            or_(Cupom.usos_restantes.is_(None), Cupom.usos_restantes > 0),
        )
        .values(
            usos_restantes=(
                Cupom.usos_restantes - 1
            )
        )
        .execution_options(synchronize_session=False)
    )
    return result.rowcount > 0