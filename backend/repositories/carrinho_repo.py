from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete, update
from database.models import ItemCarrinho


async def itens_ativos(db: AsyncSession, usuario_id: int) -> list[ItemCarrinho]:
    return list((await db.scalars(
        select(ItemCarrinho)
        .where(ItemCarrinho.id_usuario == usuario_id, ItemCarrinho.status == "em processo")
        .order_by(ItemCarrinho.criado_em)
    )).all())

async def total(db: AsyncSession, usuario_id: int) -> float:
    r = await db.scalar(
        select(func.coalesce(func.sum(ItemCarrinho.valor_total), 0))
        .where(ItemCarrinho.id_usuario == usuario_id, ItemCarrinho.status == "em processo")
    )
    return float(r or 0)

async def contador(db: AsyncSession, usuario_id: int) -> int:
    r = await db.scalar(
        select(func.count(ItemCarrinho.id))
        .where(ItemCarrinho.id_usuario == usuario_id, ItemCarrinho.status == "em processo")
    )
    return int(r or 0)

async def buscar_item(db: AsyncSession, item_id: int, usuario_id: int) -> ItemCarrinho | None:
    return await db.scalar(
        select(ItemCarrinho).where(ItemCarrinho.id == item_id, ItemCarrinho.id_usuario == usuario_id)
    )

async def buscar_existente(db: AsyncSession, usuario_id: int, produto_id: int, plano: str) -> ItemCarrinho | None:
    return await db.scalar(
        select(ItemCarrinho).where(
            ItemCarrinho.id_usuario == usuario_id, ItemCarrinho.id_produto == produto_id,
            ItemCarrinho.plano == plano, ItemCarrinho.status == "em processo",
        )
    )

async def adicionar(db: AsyncSession, dados: dict) -> ItemCarrinho:
    item = ItemCarrinho(**dados); db.add(item)
    await db.flush(); await db.refresh(item)
    return item

async def atualizar_item(db: AsyncSession, item_id: int, quantidade: int, valor_total: Decimal) -> None:
    await db.execute(
        update(ItemCarrinho).where(ItemCarrinho.id == item_id)
        .values(quantidade=quantidade, valor_total=valor_total)
    )

async def remover_itens(db: AsyncSession, usuario_id: int, ids: list[int]) -> int:
    r = await db.execute(
        delete(ItemCarrinho).where(ItemCarrinho.id_usuario == usuario_id, ItemCarrinho.id.in_(ids))
    )
    return r.rowcount

async def finalizar_itens(db: AsyncSession, usuario_id: int, ids: list[int]) -> None:
    await db.execute(
        update(ItemCarrinho)
        .where(ItemCarrinho.id_usuario == usuario_id, ItemCarrinho.id.in_(ids))
        .values(status="finalizado")
    )

async def limpar_ativos(db: AsyncSession, usuario_id: int) -> None:
    await db.execute(
        delete(ItemCarrinho)
        .where(ItemCarrinho.id_usuario == usuario_id, ItemCarrinho.status == "em processo")
    )

async def buscar_por_ids(db: AsyncSession, usuario_id: int, ids: list[int]) -> list[ItemCarrinho]:
    return list((await db.scalars(
        select(ItemCarrinho).where(
            ItemCarrinho.id_usuario == usuario_id,
            ItemCarrinho.status == "em processo",
            ItemCarrinho.id.in_(ids),
        )
    )).all())

async def inserir_guest(db: AsyncSession, itens: list[dict], usuario_id: int) -> int:
    count = 0
    for item in itens:
        existente = await buscar_existente(db, usuario_id, item["id_produto"], item.get("plano", "mensal"))
        if existente:
            nova_qtd = existente.quantidade + item.get("quantidade", 1)
            await atualizar_item(db, existente.id, nova_qtd, existente.valor_unitario * nova_qtd)
        else:
            db.add(ItemCarrinho(
                id_usuario=usuario_id, id_produto=item["id_produto"],
                nome_produto=item.get("nome_produto", ""), descricao=item.get("descricao"),
                plano=item.get("plano", "mensal"), quantidade=item.get("quantidade", 1),
                valor_unitario=Decimal(str(item.get("valor_unitario", 0))),
                valor_total=Decimal(str(item.get("valor_total", 0))),
                status="em processo",
            ))
        count += 1
    await db.flush()
    return count