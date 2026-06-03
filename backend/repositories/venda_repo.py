from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
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
    ticket_medio    = round(faturamento / total_vendas, 2) if total_vendas else 0.0

    # Produtos mais vendidos
    mais_vendidos = (await db.execute(
        select(
            Produto.id, Produto.nome, Produto.tipo,
            func.sum(ItemVenda.quantidade).label("qtd"),
            func.sum(ItemVenda.valor_total).label("fat"),
        )
        .join(ItemVenda, ItemVenda.id_produto == Produto.id)
        .group_by(Produto.id, Produto.nome, Produto.tipo)
        .order_by(func.sum(ItemVenda.quantidade).desc())
        .limit(10)
    )).all()

    # Vendas por mês (últimos 12 meses)
    vendas_mes_raw = (await db.execute(
        select(
            extract('year', Venda.data).label("ano"),
            extract('month', Venda.data).label("mes"),
            func.count(Venda.id).label("total_vendas"),
            func.sum(Venda.valor_total).label("faturamento"),
        )
        .group_by("ano", "mes")
        .order_by("ano", "mes")
        .limit(12)
    )).all()

    # Resumo por tipo de produto
    resumo_tipo_raw = (await db.execute(
        select(
            Produto.tipo,
            func.sum(ItemVenda.quantidade).label("qtd"),
            func.sum(ItemVenda.valor_total).label("fat"),
        )
        .join(ItemVenda, ItemVenda.id_produto == Produto.id)
        .group_by(Produto.tipo)
    )).all()

    # Últimas vendas
    ultimas = list((await db.scalars(
        select(Venda)
        .options(selectinload(Venda.itens).joinedload(ItemVenda.produto))
        .order_by(Venda.data.desc())
        .limit(20)
    )).all())

    return {
        "estatisticas": {
            "total_vendas": total_vendas,
            "faturamento_total": faturamento,
            "clientes_unicos": clientes_unicos,
            "ticket_medio": ticket_medio,
        },
        "produtos_mais_vendidos": [
            {
                "id": r.id,
                "nome": r.nome or f"Produto {r.id}",
                "tipo": r.tipo or "",
                "quantidade": int(r.qtd or 0),
                "faturamento": float(r.fat or 0),
            }
            for r in mais_vendidos
        ],
        "vendas_por_mes": {
            f"{int(r.ano)}-{int(r.mes):02d}": {
                "vendas": int(r.total_vendas or 0),
                "faturamento": float(r.faturamento or 0),
            }
            for r in vendas_mes_raw
        },
        "resumo_por_tipo": {
            (r.tipo or "Sem tipo"): {
                "quantidade": int(r.qtd or 0),
                "faturamento": float(r.fat or 0),
            }
            for r in resumo_tipo_raw
        },
        "ultimas_vendas": [
            {
                "id_compra": v.id,
                "data": v.data.isoformat(),
                "valor_total": float(v.valor_total),
                "nome_produto": v.itens[0].produto.nome if v.itens and v.itens[0].produto else "—",
                "tipo_produto": v.itens[0].produto.tipo if v.itens and v.itens[0].produto else "—",
                "quantidade": sum(i.quantidade for i in v.itens),
                "itens": [
                    {
                        "id_produto": i.id_produto,
                        "nome_produto": i.produto.nome if i.produto else "—",
                        "tipo_produto": i.produto.tipo if i.produto else "—",
                        "quantidade": i.quantidade,
                        "plano": i.plano,
                        "valor_unitario": float(i.valor_unitario),
                        "valor_total": float(i.valor_total),
                    }
                    for i in v.itens
                ],
            }
            for v in ultimas
        ],
    }