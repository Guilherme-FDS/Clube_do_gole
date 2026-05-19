from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from database.models import Venda, Produto


async def criar(db: AsyncSession, dados: dict) -> Venda:
    v = Venda(**dados); db.add(v); await db.flush()
    return v

async def pedidos_do_usuario(db: AsyncSession, usuario_id: int) -> list[Venda]:
    return list((await db.scalars(
        select(Venda).options(joinedload(Venda.produto))
        .where(Venda.id_usuario == usuario_id).order_by(Venda.data.desc())
    )).all())

async def buscar(db: AsyncSession, venda_id: int) -> Venda | None:
    return await db.scalar(
        select(Venda).options(joinedload(Venda.produto), joinedload(Venda.cliente))
        .where(Venda.id == venda_id)
    )

async def pedidos_do_cliente_admin(db: AsyncSession, usuario_id: int) -> list[dict]:
    vendas = list((await db.scalars(
        select(Venda).options(joinedload(Venda.produto))
        .where(Venda.id_usuario == usuario_id).order_by(Venda.data.desc())
    )).all())
    return [
        {
            "id": v.id,
            "id_produto": v.id_produto,
            "nome_produto": v.produto.nome if v.produto else "Produto removido",
            "quantidade": v.quantidade,
            "plano": v.plano,
            "data": v.data.isoformat(),
            "valor_total": float(v.valor_total),
            "valor_sem_desconto": float(v.valor_original or 0),
            "desconto_aplicado": float(v.desconto_aplicado or 0),
            "valor_desconto": float(v.valor_desconto or 0),
            "cupom_aplicado": v.cupom_aplicado or "",
            "economia": float((v.valor_original or 0) - v.valor_total),
        }
        for v in vendas
    ]

async def dashboard(db: AsyncSession) -> dict:
    total_vendas    = await db.scalar(select(func.count(Venda.id))) or 0
    faturamento     = float(await db.scalar(select(func.sum(Venda.valor_total))) or 0)
    clientes_unicos = await db.scalar(select(func.count(func.distinct(Venda.id_usuario)))) or 0

    mais_vendidos = (await db.execute(
        select(Produto.id, Produto.nome,
               func.sum(Venda.quantidade).label("qtd"),
               func.sum(Venda.valor_total).label("fat"))
        .join(Produto, Venda.id_produto == Produto.id, isouter=True)
        .group_by(Venda.id_produto, Produto.id, Produto.nome)
        .order_by(func.sum(Venda.quantidade).desc()).limit(10)
    )).all()

    ultimas = list((await db.scalars(
        select(Venda).options(joinedload(Venda.produto)).order_by(Venda.data.desc()).limit(10)
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
            {"id": v.id, "id_produto": v.id_produto,
             "nome_produto": v.produto.nome if v.produto else "—",
             "quantidade": v.quantidade, "valor_total": float(v.valor_total),
             "plano": v.plano, "data": v.data.isoformat()}
            for v in ultimas
        ],
    }