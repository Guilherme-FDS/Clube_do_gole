from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Produto


async def listar(db: AsyncSession, tipo: str | None = None) -> list[Produto]:
    q = select(Produto).where(Produto.ativo == True)
    if tipo: q = q.where(Produto.tipo == tipo.lower())
    return list((await db.scalars(q.order_by(Produto.id))).all())

async def listar_admin(db: AsyncSession) -> list[Produto]:
    return list((await db.scalars(select(Produto).order_by(Produto.id))).all())

async def buscar(db: AsyncSession, produto_id: int) -> Produto | None:
    return await db.get(Produto, produto_id)

async def criar(db: AsyncSession, dados: dict) -> Produto:
    p = Produto(**dados); db.add(p)
    await db.flush(); await db.refresh(p)
    return p

async def atualizar(db: AsyncSession, produto_id: int, dados: dict) -> Produto | None:
    p = await db.get(Produto, produto_id)
    if not p: return None
    for k, v in dados.items(): setattr(p, k, v)
    await db.flush(); await db.refresh(p)
    return p

async def remover(db: AsyncSession, produto_id: int) -> bool:
    p = await db.get(Produto, produto_id)
    if not p: return False
    await db.delete(p); await db.flush()
    return True

async def decrementar_estoque(db: AsyncSession, produto_id: int, qtd: int) -> None:
    pass