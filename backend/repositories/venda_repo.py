from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from database.models import Venda, ItemVenda, Produto


async def criar(db: AsyncSession, dados_venda: dict, itens: list[dict]) -> Venda:
    v = Venda(**dados_venda)
    db.add(v)
    await db.flush()
    for item in itens:
        db.add(ItemVenda(id_venda=v.id, **item))
    await db.flush()
    return v


async def pedidos_do_usuario(db: AsyncSession, usuario_id: int) -> list[Venda]:
    return list((await db.scalars(
        select(Venda)
        .options(selectinload(Venda.itens).joinedload(ItemVenda.produto))
        .where(Venda.id_usuario == usuario_id)
        .order_by(Venda.data.desc())
    )).all())


async def buscar(db: AsyncSession, venda_id: int) -> Venda | None:
    return await db.scalar(
        select(Venda)
        .options(selectinload(Venda.itens).joinedload(ItemVenda.produto), joinedload(Venda.cliente))
        .where(Venda.id == venda_id)
    )


async def pedidos_do_cliente_admin(db: AsyncSession, usuario_id: int) -> list[dict]:
    vendas = list((await db.scalars(
        select(Venda)
        .options(selectinload(Venda.itens).joinedload(ItemVenda.produto))
        .where(Venda.id_usuario == usuario_id)
        .order_by(Venda.data.desc())
    )).all())
    return [
        {
            "id": v.id,
            "data": v.data.isoformat(),
            "valor_total": float(v.valor_total),
            "valor_sem_desconto": float(v.valor_original or 0),
            "desconto_aplicado": float(v.desconto_aplicado or 0),
            "valor_desconto": float(v.valor_desconto or 0),
            "cupom_aplicado": v.cupom_aplicado or "",
            "economia": float((v.valor_original or 0) - v.valor_total),
            "itens": [
                {
                    "id_produto": i.id_produto,
                    "nome_produto": i.produto.nome if i.produto else "Produto removido",
                    "quantidade": i.quantidade,
                    "plano": i.plano,
                    "valor_unitario": float(i.valor_unitario),
                    "valor_total": float(i.valor_total),
                }
                for i in v.itens
            ],
        }
        for v in vendas
    ]


async def dashboard(db: AsyncSession) -> dict:
    total_vendas    = await db.scalar(select(func.count(Venda.id))) or 0
    faturamento     = float(await db.scalar(select(func.sum(Venda.valor_total))) or 0)
    clientes_unicos = await db.scalar(select(func.count(func.distinct(Venda.id_usuario)))) or 0

    mais_vendidos = (await db.execute(
        select(
            Produto.id, Produto.nome,
            func.sum(ItemVenda.quantidade).label("qtd"),
            func.sum(ItemVenda.valor_total).label("fat"),
        )
        .join(ItemVenda, ItemVenda.id_produto == Produto.id)
        .group_by(Produto.id, Produto.nome)
        .order_by(func.sum(ItemVenda.quantidade).desc())
        .limit(10)
    )).all()

    ultimas = list((await db.scalars(
        select(Venda)
        .options(selectinload(Venda.itens).joinedload(ItemVenda.produto))
        .order_by(Venda.data.desc())
        .limit(10)
    )).all())

    return {
        "total_vendas": total_vendas,
        "faturamento_total": faturamento,
        "clientes_unicos": clientes_unicos,
        "produtos_mais_vendidos": [
            {"id": r.id, "nome": r.nome or f"Produto {r.id}",
             "quantidade": int(r.qtd or 0), "faturamento": float(r.fat or 0)}
            for r in mais_vendidos
        ],
        "ultimas_vendas": [
            {
                "id": v.id,
                "data": v.data.isoformat(),
                "valor_total": float(v.valor_total),
                "itens": [
                    {"id_produto": i.id_produto,
                     "nome_produto": i.produto.nome if i.produto else "—",
                     "quantidade": i.quantidade,
                     "plano": i.plano}
                    for i in v.itens
                ],
            }
            for v in ultimas
        ],
    }