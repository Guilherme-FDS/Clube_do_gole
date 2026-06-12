# services/estoque_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models import Produto
from repositories import estoque_repo


async def entrada(db: AsyncSession, id_produto: int, quantidade: int, motivo: str = "entrada manual") -> dict:
    return await _movimentar(db, id_produto, "entrada", quantidade, motivo)


async def saida(db: AsyncSession, id_produto: int, quantidade: int, motivo: str = "saida manual", id_venda: int = None) -> dict:
    return await _movimentar(db, id_produto, "saida", quantidade, motivo, id_venda)


async def ajuste(db: AsyncSession, id_produto: int, quantidade: int, motivo: str = "ajuste manual") -> dict:
    return await _movimentar(db, id_produto, "ajuste", quantidade, motivo)


async def _movimentar(db: AsyncSession, id_produto: int, tipo: str, quantidade: int, motivo: str, id_venda: int = None) -> dict:
    produto = await db.get(Produto, id_produto)
    if not produto:
        raise ValueError("Produto não encontrado.")

    saldo_anterior = await estoque_repo.saldo_atual(db, id_produto)

    if tipo == "entrada":
        saldo_posterior = saldo_anterior + quantidade
    elif tipo == "saida":
        if saldo_anterior < quantidade:
            raise ValueError("Estoque insuficiente.")
        saldo_posterior = saldo_anterior - quantidade
    elif tipo == "ajuste":
        saldo_posterior = quantidade
    else:
        raise ValueError("Tipo de movimentação inválido.")

    await estoque_repo.registrar(db, {
        "id_produto": id_produto,
        "tipo": tipo,
        "quantidade": quantidade,
        "saldo_anterior": saldo_anterior,
        "saldo_posterior": saldo_posterior,
        "motivo": motivo,
        "id_venda": id_venda,
    })

    return {
        "id_produto": id_produto,
        "tipo": tipo,
        "saldo_anterior": saldo_anterior,
        "saldo_posterior": saldo_posterior,
    }


async def listar_movimentacoes(db: AsyncSession) -> list[dict]:
    movs = await estoque_repo.listar_todas(db)
    return [_serializar(m) for m in movs]


async def listar_por_produto(db: AsyncSession, id_produto: int) -> list[dict]:
    movs = await estoque_repo.listar_por_produto(db, id_produto)
    return [_serializar(m) for m in movs]


def _serializar(m) -> dict:
    return {
        "id": m.id,
        "id_produto": m.id_produto,
        "nome_produto": m.produto.nome if m.produto else None,
        "tipo": m.tipo,
        "quantidade": m.quantidade,
        "saldo_anterior": m.saldo_anterior,
        "saldo_posterior": m.saldo_posterior,
        "motivo": m.motivo,
        "id_venda": m.id_venda,
        "criado_em": m.criado_em.isoformat(),
    }