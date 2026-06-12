# repositories/estoque_repo.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from database.models import MovimentacaoEstoque, Produto


async def registrar(db: AsyncSession, dados: dict) -> MovimentacaoEstoque:
    mov = MovimentacaoEstoque(**dados)
    db.add(mov)
    await db.flush()
    return mov


async def listar_por_produto(db: AsyncSession, id_produto: int) -> list[MovimentacaoEstoque]:
    result = await db.execute(
        select(MovimentacaoEstoque)
        .options(joinedload(MovimentacaoEstoque.produto))
        .where(MovimentacaoEstoque.id_produto == id_produto)
        .order_by(MovimentacaoEstoque.criado_em.desc())
    )
    return result.scalars().all()


async def saldo_atual(db: AsyncSession, id_produto: int) -> int:
    """Saldo derivado da última movimentação (estoque não vive mais em Produto)."""
    ultima = await db.scalar(
        select(MovimentacaoEstoque.saldo_posterior)
        .where(MovimentacaoEstoque.id_produto == id_produto)
        .order_by(MovimentacaoEstoque.id.desc())
        .limit(1)
    )
    return ultima or 0


async def listar_todas(db: AsyncSession) -> list[MovimentacaoEstoque]:
    result = await db.execute(
        select(MovimentacaoEstoque)
        .options(joinedload(MovimentacaoEstoque.produto))
        .order_by(MovimentacaoEstoque.criado_em.desc())
    )
    return result.scalars().all()