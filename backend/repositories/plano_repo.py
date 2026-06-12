# repositories/plano_repo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import PlanoAssinatura
from sqlalchemy import case


async def listar_por_produto(db: AsyncSession, produto_id: int, apenas_ativos: bool = True) -> list[PlanoAssinatura]:
    ordem = case(
        (PlanoAssinatura.recorrencia == 'mensal', 1),
        (PlanoAssinatura.recorrencia == 'semestral', 2),
        (PlanoAssinatura.recorrencia == 'anual', 3),
        else_=4
    )
    q = select(PlanoAssinatura).where(PlanoAssinatura.id_produto == produto_id)
    if apenas_ativos:
        q = q.where(PlanoAssinatura.ativo == True)
    return list((await db.scalars(q.order_by(ordem))).all())


async def buscar(db: AsyncSession, plano_id: int) -> PlanoAssinatura | None:
    return await db.get(PlanoAssinatura, plano_id)


async def criar(db: AsyncSession, dados: dict) -> PlanoAssinatura:
    p = PlanoAssinatura(**dados)
    db.add(p)
    await db.flush()
    await db.refresh(p)
    return p


async def atualizar(db: AsyncSession, plano_id: int, dados: dict) -> PlanoAssinatura | None:
    p = await db.get(PlanoAssinatura, plano_id)
    if not p:
        return None
    for k, v in dados.items():
        setattr(p, k, v)
    await db.flush()
    await db.refresh(p)
    return p


async def remover(db: AsyncSession, plano_id: int) -> bool:
    p = await db.get(PlanoAssinatura, plano_id)
    if not p:
        return False
    await db.delete(p)
    await db.flush()
    return True